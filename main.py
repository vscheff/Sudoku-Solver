import controller as c


def main():
    control = c.Control()
    control.initialize()
    control.main_loop()


if __name__ == '__main__':
    main()
