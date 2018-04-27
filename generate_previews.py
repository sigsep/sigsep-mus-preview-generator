from __future__ import division
import musdb
import argparse
import csv


def generate_previews(mus, preview_file, output_dir=None):

    with open(preview_file, 'r') as csvfile:

        previews = csv.reader(csvfile, delimiter=',')

        for preview in previews:

            track_name, start_sample, end_sample, _, _ = preview

            try:
                track = mus.load_mus_tracks(tracknames=[track_name])[0]
            except:
                print("Can't find track: {}".format(track_name))
                continue

            print(track)

            cropped_track = crop_track(track, start_sample, end_sample)

            if output_dir is not None:

                mus._save_estimates(
                    cropped_track,
                    track,
                    estimates_dir=output_dir
                )


def crop_track(track, start_pos, end_pos):
    start_pos, end_pos = int(start_pos), int(end_pos)
    estimates = {}
    # crop target track and save it as estimate
    for target_name, target_track in track.targets.items():
        estimates[target_name] = target_track.audio[start_pos:end_pos]

    estimates['mixture'] = track.audio[start_pos:end_pos]
    return estimates


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--musdb',
        help='Path to musdb',
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

    parser.add_argument(
        '--iswav',
        help='Read musdb wav instead of stems',
        action='store_true',
    )

    args = parser.parse_args()

    mus = musdb.DB(args.musdb, is_wav=args.iswav)

    generate_previews(mus, args.previews, args.o)
