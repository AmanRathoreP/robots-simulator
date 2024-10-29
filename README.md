<div align="center">
  <h1>Robot Simulator</h1>
</div>

<p align="center">
  Classes of this repository helps users to simulate maze-solving, line-follower, and other types of robots in an realistic physics environment.
</p>

# Features

* Load mazes from PNG/SVG files, with walls as black pixels and open spaces as white pixels.
* Multiple sensors like IR and LIDAR are supported, more can be created by inheriting Sensors class
* Customizable LIDAR sensor positions and angles for enhanced detection.
* Realistic movement dynamics using Pymunk for accurate simulation.
* Class-based design allowing easy customization of robot behavior.
* Integration with friction handling for realistic floor interactions.

# Quick start

Run the below commands one by one

* Cloning the repository
  ```
  git clone -b master https://github.com/AmanRathoreP/robots-simulator.git
  ```
* Navigating to the project's directory
  ```
  cd "robots-simulator"
  ```
* Creating python's virtual environment
  ```
  python -m venv python_virtual_environment_for_simulator
  ```
* Activating `python_virtual_environment_for_simulator` virtual environment
  ```
  python_virtual_environment_for_simulator\Scripts\activate
  ```
* Adding/Downloading necessary packages
  ```
  pip install -r requirements.txt
  ```
* Run provided examples using below command
  ```
  python examples\01_human_controlled.py
  ```

# Contributing [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](issues.md)

Thank you for considering contributing to the Maze Solver Simulator!

Please note that we have a code of conduct; kindly follow it in all your interactions with the program files.

We welcome any type of contribution, _not only code_. You can help with:
- **QA**: File bug reports; the more details you can provide, the better (e.g., images or videos).
- **New Features**: Suggest modifications or request enhancements to existing features.
- **Code**: Check the [open issues](issues.md). Even if you can't write the code yourself, commenting on them shows you care about a given issue.

# Demo
...
# Author

- [@Aman](https://www.github.com/AmanRathoreP)
   - [GitHub](https://www.github.com/AmanRathoreP)
   - [Telegram](https://t.me/aman0864)
   - Email -> *aman.proj.rel@gmail.com*

# Facts
* The project was started in October 2024, aimed at providing a robust platform for testing and understanding different algorithms to control robots in different environments.
* The Maze Solver Simulator is designed for users interested in robotics and algorithmic problem-solving, providing a realistic testing environment.

# License

[GNU Affero General Public License v3.0](https://choosealicense.com/licenses/agpl-3.0/) | [LICENSE](LICENSE/)

Copyright (c) 2024, Aman Rathore