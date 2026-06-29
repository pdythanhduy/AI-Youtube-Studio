#!/usr/bin/env python3
"""Render/assembly stage: TTS audio + beat images -> a motion video (Hashima-style).

Audio-driven: concatenate the per-segment Vbee mp3s into one narration track, measure
its real duration, spread the beat images across that timeline. Each image becomes a
1920x1080 clip with a slow **Ken Burns** zoom + fade in/out (so it is not static); the
first clip carries a fading **title card** overlay. Clips are concatenated and the
narration muxed on top.

Inputs:  projects/<slug>/assets/audio/seg_NN.mp3, assets/images/beat_NN.jpg
Output:  projects/<slug>/export/rough/<slug>_rough.mp4

Audio is paced (each segment keeps its [PAUSE] gap from voice_script) and a low ambience
bed is mixed under the narration (a provided assets/ambience.* file, else a synthesized
rumble). Motion-graphic data cards remain the polish backlog.

Usage: python tools/render/assemble_video.py --project <slug>
       [--no-ambience] [--ambience FILE] [--no-motion]
"""
from __future__ import annotations
import argparse, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROJECTS = REPO / "projects"
W, H, FPS = 1920, 1080, 30


def numkey(p: Path) -> int:
    m = re.search(r"(\d+)", p.stem)
    return int(m.group(1)) if m else 0


def run(cmd: list[str], cwd: str | None = None) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if r.returncode != 0:
        sys.exit(f"[ffmpeg ERROR] {' '.join(cmd[:8])}...\n{r.stderr[-900:]}")


def duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nk=1:nw=1", str(path)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def serif_font() -> str | None:
    """Cross-platform JP serif font file (Windows VF or Linux Noto Serif CJK)."""
    cands = [r"C:\Windows\Fonts\NotoSerifJP-VF.ttf",
             "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
             "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"]
    for c in cands:
        if Path(c).exists():
            return c
    return None


def title_text(proj: Path) -> str:
    inp = proj / "input.json"
    if inp.exists():
        try:
            return json.loads(inp.read_text(encoding="utf-8")).get("topic", proj.name)
        except Exception:
            pass
    return proj.name


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Assemble TTS audio + beat images into a motion video")
    ap.add_argument("--project", required=True)
    ap.add_argument("--no-motion", action="store_true", help="disable Ken Burns (static fallback)")
    ap.add_argument("--no-ambience", action="store_true", help="disable the background ambience bed")
    ap.add_argument("--ambience", help="ambience audio file to use (else synthesized)")
    ap.add_argument("--no-cards", action="store_true", help="disable the title + chapter MG cards")
    a = ap.parse_args()
    proj = PROJECTS / a.project
    audio = sorted((proj / "assets" / "audio").glob("seg_*.mp3"), key=numkey)
    images = sorted((proj / "assets" / "images").glob("beat_*.jpg"), key=numkey) \
        + sorted((proj / "assets" / "images").glob("beat_*.png"), key=numkey)
    if not audio:
        sys.exit("[ERROR] no assets/audio/seg_*.mp3 (run tts_generate.py first)")
    if not images:
        sys.exit("[ERROR] no assets/images/beat_*.jpg (run generate_images.py first)")

    work = Path(tempfile.mkdtemp(prefix="assemble_", dir=str(proj)))
    try:
        # 1) narration — pace each segment with its trailing [PAUSE] gap, then lay an ambience bed
        amf = proj / "audio_manifest.json"
        items: list[list] = []
        manifest_has_pause = False
        if amf.exists():
            data = json.loads(amf.read_text(encoding="utf-8"))
            segs_m = sorted(data.get("segments", []), key=lambda x: x.get("seg", 0))
            manifest_has_pause = any("pause_after" in s for s in segs_m)
            for s in segs_m:
                f = proj / s["file"]
                if f.exists():
                    items.append([f, float(s.get("pause_after", 0.35))])
        if not items:
            items = [[p, 0.35] for p in audio]   # no manifest -> uniform breathing gap
        # fallback: if the manifest predates pacing, derive pauses from voice_script.txt
        if not manifest_has_pause and (proj / "voice_script.txt").exists():
            try:
                sys.path.insert(0, str(REPO / "tools" / "audio"))
                from tts_generate import segments_from_voice
                vp = [s["pause_after"] for s in segments_from_voice((proj / "voice_script.txt").read_text(encoding="utf-8"))]
                if len(vp) == len(items):
                    for it, p in zip(items, vp):
                        it[1] = p
            except Exception:
                pass
        # pad each segment with its pause; normalize params so concat -c copy is safe
        padded = []
        for i, (f, pause) in enumerate(items):
            pf = work / f"a_{i:04d}.m4a"
            af = f"apad=pad_dur={pause:.2f}" if pause > 0 else "anull"
            run(["ffmpeg", "-y", "-i", str(f), "-af", af, "-ar", "44100", "-ac", "2",
                 "-c:a", "aac", "-b:a", "192k", str(pf)])
            padded.append(pf)
        alist = work / "audio.txt"
        alist.write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in padded), encoding="utf-8")
        voice_track = work / "voice.m4a"
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(alist), "-c", "copy", str(voice_track)])
        total = duration(voice_track)
        if total <= 0:
            sys.exit("[ERROR] narration has zero duration")

        narration = voice_track
        amb_label = "no ambience"
        if not a.no_ambience:
            amb_src = (Path(a.ambience) if a.ambience else
                       next((c for c in [proj / "assets" / "ambience.mp3", proj / "assets" / "ambience.wav",
                                         REPO / "assets" / "ambience.mp3"] if c.exists()), None))
            amb = work / "amb.m4a"
            if amb_src:
                amb_label = f"ambience({Path(amb_src).name})"
                run(["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(amb_src), "-t", f"{total:.2f}",
                     "-af", "volume=0.18", "-ar", "44100", "-ac", "2", "-c:a", "aac", str(amb)])
            else:  # synthesize a quiet, low-passed rumble bed (dark-documentary atmosphere)
                amb_label = "ambience(synth)"
                run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anoisesrc=color=brown:amplitude=0.7:r=44100",
                     "-t", f"{total:.2f}", "-af", "highpass=f=40,lowpass=f=320,volume=0.06",
                     "-ac", "2", "-c:a", "aac", str(amb)])
            narration = work / "narration.m4a"
            run(["ffmpeg", "-y", "-i", str(voice_track), "-i", str(amb), "-filter_complex",
                 "[0:a][1:a]amix=inputs=2:duration=first:normalize=0[a]", "-map", "[a]",
                 "-c:a", "aac", "-b:a", "192k", str(narration)])
            total = duration(narration)
        print(f"audio: {len(items)} paced segs | {amb_label} | total {total:.1f}s")

        n = len(images)
        # build the visual sequence: opening title card + images interleaved with chapter cards
        # (cards consume timeline; narration plays over them, so audio stays in sync)
        TITLE_D, CH_D = 3.6, 2.7
        sequence: list[tuple[str, Path, float]] = []
        ch_at: dict[int, list[Path]] = {}
        use_cards = not a.no_cards
        card_time = 0.0
        if use_cards:
            try:
                sys.path.insert(0, str(REPO / "tools" / "visuals"))
                import render_cards as RC
                if not RC.font_path():
                    raise RuntimeError("no font for cards")
                tc = work / "card_title.jpg"
                RC.render_title_card(proj, tc)
                chapters = RC.parse_chapters(proj)
                plan_total = max((s for s, _ in chapters), default=0) or 1
                for k, (sec, ctitle) in enumerate(chapters[1:], start=2):  # skip ch1 (title card covers intro)
                    cc = work / f"card_ch{k:02d}.jpg"
                    RC.render_chapter_card(proj, k, len(chapters), ctitle, cc)
                    idx = min(n - 1, max(1, round(sec / plan_total * n)))
                    ch_at.setdefault(idx, []).append(cc)
                card_time = TITLE_D + sum(len(v) for v in ch_at.values()) * CH_D
                sequence.append(("card", tc, TITLE_D))
            except Exception as e:
                print(f"[WARN] MG cards disabled: {e}")
                use_cards = False
        per = round((total - card_time) / n, 3)
        for i, img in enumerate(images):
            for cc in ch_at.get(i, []):
                sequence.append(("card", cc, CH_D))
            d = round(total - card_time - per * (n - 1), 3) if i == n - 1 else per
            sequence.append(("image", img, d))
        ncards = sum(1 for k, _, _ in sequence if k == "card")
        print(f"sequence: {len(sequence)} clips ({ncards} cards + {n} images) | total {total:.1f}s")

        font = serif_font()  # only for the no-cards title-overlay fallback
        if font and not use_cards:
            shutil.copy(font, work / "f.ttf")
            (work / "title.txt").write_text(title_text(proj), encoding="utf-8")

        clips = []
        for i, (kind, src, d) in enumerate(sequence):
            clip = work / f"clip_{i:03d}.mp4"
            if a.no_motion:
                vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},format=yuv420p"
            elif kind == "card":  # gentle zoom + fade (cards are already 1920x1080)
                vf = (f"scale=2200:-1,zoompan=z='min(max(pzoom,1)+0.0004,1.07)':d=1:"
                      f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
                      f"trim=duration={d},fade=t=in:st=0:d=0.5,fade=t=out:st={max(0.1, d-0.5):.2f}:d=0.5,format=yuv420p")
            else:  # Ken Burns slow zoom-in + fade
                vf = (f"scale=2400:-1,zoompan=z='min(max(pzoom,1)+0.0008,1.16)':d=1:"
                      f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
                      f"trim=duration={d},fade=t=in:st=0:d=0.7,fade=t=out:st={max(0.1, d-0.7):.2f}:d=0.7,format=yuv420p")
            if kind == "image" and i == 0 and font and not use_cards:  # title overlay fallback
                vf += (f",drawtext=fontfile=f.ttf:textfile=title.txt:fontcolor=white:fontsize=70:"
                       f"x=(w-text_w)/2:y=h*0.70:box=1:boxcolor=black@0.45:boxborderw=26:"
                       f"alpha='if(lt(t,4.5),1,max(0,(6-t)/1.5))'")
            run(["ffmpeg", "-y", "-loop", "1", "-i", str(src.resolve()), "-t", f"{d}", "-r", str(FPS),
                 "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", str(clip)],
                cwd=str(work))
            clips.append(clip)
            print(f"  clip {i+1}/{len(sequence)}: [{kind}] {src.name} ({d:.1f}s)")

        clist = work / "clips.txt"
        clist.write_text("".join(f"file '{c.resolve().as_posix()}'\n" for c in clips), encoding="utf-8")
        video_raw = work / "video_raw.mp4"
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(clist), "-c", "copy", str(video_raw)])

        out = proj / "export" / "rough" / f"{a.project}_rough.mp4"
        out.parent.mkdir(parents=True, exist_ok=True)
        run(["ffmpeg", "-y", "-i", str(video_raw), "-i", str(narration),
             "-c:v", "copy", "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(out)])
        print(f"\nRendered: {out.relative_to(proj)} ({duration(out):.1f}s, {out.stat().st_size/1048576:.1f} MB)")
        return 0
    finally:
        for f in work.glob("*"):
            f.unlink(missing_ok=True)
        work.rmdir()


if __name__ == "__main__":
    raise SystemExit(main())
