from seekr.core import SeekrCli

if __name__ == "__main__":
    seekr_cli = SeekrCli()
    seekr_cli.parse()
    seekr_cli.exec()
