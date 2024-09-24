from create_newsletter import NewsLetterHandler

# TODO create a test file that creates a docker container
# and runs the image in a development environment

def main() -> None:
    newsletter = NewsLetterHandler()
    newsletter.run()

if __name__ == "__main__":
    main()