import subprocess
import os
import argparse
from glob import iglob

from matplotlib.style import available


def get_lesson(lesson_dir, desired_lesson_number, exercise=False):
    # get lessons from the lessons directory
    found_lessons = []
    for lesson_notebook in iglob(os.path.join(lesson_dir, f'*{"_ex" if exercise else ""}.ipynb')):
        lesson_number = int(os.path.basename(lesson_notebook).split('_')[0])
        if lesson_number == desired_lesson_number:
            return lesson_notebook
        else:
            found_lessons.append(os.path.basename(lesson_notebook))

    available_lessons = '\n'.join([f'\t {i:d} - {lesson}' for i, lesson in enumerate(found_lessons, start=1)])
    raise ValueError(f'Could not find lesson "{desired_lesson_number}". Available lessons:\n{available_lessons}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=8888, type=int)
    parser.add_argument('lesson_number', type=int, nargs='?')
    parser.add_argument('--list', '-l', action='store_true')
    parser.add_argument('--exercise', '-e', action='store_true')
    args = parser.parse_args()

    package_root_dir = os.path.dirname(os.path.abspath(__file__))
    if args.exercise:
        notebook_dir = os.path.join(package_root_dir, 'exercises')
    else:
        notebook_dir = os.path.join(package_root_dir, 'lessons')

    if args.list:
        print(f"Available {'lessons' if not args.exercise else 'exercises'} (<number> - <name>):")
        print('\n'.join([f"\t{i} - {os.path.basename(notebook)}" for i, notebook in enumerate(iglob(os.path.join(notebook_dir, '*.ipynb')), start=1)]))
        return

    # Run the first lesson if no lesson number is provided
    if args.lesson_number is None or args.lesson_number == 0:
        notebook_path = os.path.join(package_root_dir, '00_intro.ipynb')
    else:
        notebook_path = get_lesson(notebook_dir, args.lesson_number, exercise=args.exercise)

    server = subprocess.Popen(['jupyter', 'notebook', '--no-browser', '--port', str(args.port), notebook_path])

    # Wait for the server
    try:
        server.wait()
    except KeyboardInterrupt:
        server.terminate()
        server.wait()
    except BaseException:
        server.kill()
        raise


if __name__ == '__main__':
    main()
