from create_newsletter import NewsLetterHandler

# TODO create a test file that checks if all environment
# variables requested in the module are being passed
# in the daily newsletter workflow and set in the environment

def main() -> None:
    newsletter = NewsLetterHandler()
    newsletter.run()

if __name__ == "__main__":
    main()