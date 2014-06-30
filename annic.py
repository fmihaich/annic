"""

ANNIC MAIN MODULE

================
This module allows user to execute the software running the following command:
    - python annic.py
----------------

@author: Florencia Mihaich
@version: 1.0
@date: June 6th, 2014

"""

from annic.ui.main.app_container import AnnicUI


def main():
    annic_ui = AnnicUI()
    annic_ui.run()

if __name__ == '__main__':
    main()