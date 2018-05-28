import argparse
import csv
from pathlib import Path as P
import soundfile as sf


def generate_previews(estimate_root_dir, preview_file, output_dir=None):

    # aggregate preview cut data
    prev_data = {}
    with open(preview_file, 'r') as csvfile:
        previews = csv.reader(csvfile, delimiter=',')
        for preview in previews:
            track_name, start_sample, end_sample, _, _ = preview
            prev_data[track_name] = {
                'start': int(start_sample),
                'end': int(end_sample)
            }

    p = P(estimate_root_dir)
    if p.exists():
        for track in p.glob('*/*'):
            if track.is_dir():
                for target in track.glob('*.wav'):
                    # get cut values
                    track_cut = prev_data[track.name]
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
