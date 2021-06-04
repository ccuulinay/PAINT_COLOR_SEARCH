from paint_colors import color_collecter

import os
import pathlib
import typer
import logging


################### Get logger ###################
# set up basic config - logging to console
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s: %(name)s: %(message)s',
                    # datefmt='%m-%d %H:%M',
                    # filename='/temp/myapp.log',
                    # filemode='w'
                    )

# Create console handlers
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_format = logging.Formatter('%(levelname)s: %(asctime)s: %(name)s: %(message)s')
c_handler.setFormatter(c_format)

# Create file handler
log_f_path = os.environ.get("CLI_LOG_PATH", os.path.dirname(__file__))
log_f_p = pathlib.Path(log_f_path) / "logs"
log_f_p.mkdir(parents=True, exist_ok=True)
log_f = log_f_p / "cli.log"
f_handler = logging.FileHandler(log_f)
f_handler.setLevel(logging.ERROR)
f_format = logging.Formatter('%(levelname)s: %(asctime)s: %(name)s: %(message)s')
f_handler.setFormatter(f_format)

# Add hanlder to root logger.
logging.getLogger('').addHandler(f_handler)
# Add handlers to the logger
# logger.addHandler(c_handler)
# logger.addHandler(f_handler)

# Create a custom logger
logger = logging.getLogger("paint_color_cli")

logger.setLevel(logging.INFO)


app = typer.Typer()


@app.command()
def usage(name: str = "User"):
    typer.echo(f"Hello {name}. This is for querying paint color matching between Nippon and Dulux.")



@app.command()
def refresh_nippon_data(save_path: str = "./"):
    logger.info(f"Start getting data of nippon.")
    nippon_df = color_collecter.get_cn_nippon_cmap(save_to_local=save_path)
    logger.info(f"Total {nippon_df.shape[0]} are collected and save to path {save_path}.")


@app.command()
def refresh_dulux_data(save_path: str = "./"):
    logger.info(f"Start getting data of dulux.")
    dulux_df = color_collecter.get_cn_dulux_cmap(save_to_local=save_path)
    logger.info(f"Total {dulux_df.shape[0]} are collected and save to path {save_path}.")


if __name__ == "__main__":
    app()
