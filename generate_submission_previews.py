import argparse
import csv
from pathlib import Path as P
import soundfile as sf
import simplejson as json


def generate_previews(estimate_root_dir, preview_file, output_dir=None):
    # aggregate preview cut data
    prev_data = {}
    with open(preview_file, 'r') as csvfile:
        previews = csv.reader(csvfile, delimiter=',')
        for preview in previews:
            track_name, start_sample, end_sample, start_s, end_s = preview
            prev_data[track_name] = {
                'start': int(start_s),
                'end': int(end_s)
            }

    p = P(estimate_root_dir)
    if p.exists():
        for track in p.glob('*/*'):
            # go into audio targets
            if track.is_dir():
                print(track.stem)

                # get cut values for track
                track_cut = prev_data[track.name]

                for target in track.glob('*.wav'):
                    # read the target audio
                    audio, rate = sf.read(target)
                    # cut the audio
                    audio = audio[track_cut['start']:track_cut['end']]
                    # compose new path in different root_location
                    P_out = P(output_dir, *target.parts[-3:])
                    # re-create the path structure
                    P_out.parent.mkdir(parents=True, exist_ok=True)
                    # write out files
                    sf.write(P_out, audio, rate)

            json_file = P(str(track.absolute()) + '.json')
            with open(json_file) as json_file:
                jf = json.load(json_file)

            for j, t in enumerate(jf['targets']):
                cut_frames = []
                for k, frame in enumerate(t['frames']):
                    if (
                        frame['time'] >= track_cut['start']
                    ) and (
                        (frame['time'] + frame['duration']) <= track_cut['end']
                    ):
                        frame['time'] = frame['time'] - track_cut['start']
                        cut_frames.append(frame)

                jf['targets'][j]['frames'] = cut_frames

            json_string = json.dumps(
                jf,
                indent=2,
                allow_nan=True
            )
            J_out = P(str(P(output_dir, *target.parts[-3:-1])) + '.json')
            with open(J_out, 'w+') as f:
                f.write(json_string)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--estimate_root_dir',
        help='Path to estimate_root_dir',
        type=str,
    )

    parser.add_argument(
        '--previews',
        help='CSV file holding the cut-list',
        type=str,
    )

    parser.add_argument(
        '-o',
        help='Output directory to save the previews',
        type=str,
        required=True,
    )

    args = parser.parse_args()

    generate_previews(args.estimate_root_dir, args.previews, args.o)
