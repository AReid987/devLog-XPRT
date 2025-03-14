import argparse
import asyncio
import base64
import os
from pathlib import Path

from proxy_lite import Runner, RunnerConfig
from proxy_lite.gif_maker import create_run_gif
from proxy_lite.logger import logger


def update_config_from_env(config: RunnerConfig) -> RunnerConfig:
    if os.getenv("PROXY_LITE_API_BASE"):
        config.solver.agent.client.api_base = os.getenv("PROXY_LITE_API_BASE")
    if os.getenv("PROXY_LITE_MODEL"):
        config.solver.agent.client.model_id = os.getenv("PROXY_LITE_MODEL")
    if os.getenv("PROXY_LITE_VIEWPORT_WIDTH"):
        config.environment.viewport_width = int(os.getenv("PROXY_LITE_VIEWPORT_WIDTH"))
    if os.getenv("PROXY_LITE_VIEWPORT_HEIGHT"):
        config.environment.viewport_height = int(os.getenv("PROXY_LITE_VIEWPORT_HEIGHT"))
    return config


def do_command(args):
    do_text = " ".join(args.task)
    logger.info("🤖 Let me help you with that...")
    # Take default config from YAML
    config = RunnerConfig.from_yaml(args.config)
    # Update config from environment variables
    config = update_config_from_env(config)
    # Update config from command-line arguments
    if args.api_base:
        config.solver.agent.client.api_base = args.api_base
    if args.model:
        config.solver.agent.client.model_id = args.model
    if args.homepage:
        config.environment.homepage = args.homepage
    if args.viewport_width:
        config.environment.viewport_width = args.viewport_width
    if args.viewport_height:
        config.environment.viewport_height = args.viewport_height
    o = Runner(config=config)
    result = asyncio.run(o.run(do_text))

    final_screenshot = result.observations[-1].info["original_image"]
    path = _extracted_from_do_command_23("screenshots", result, '.png')
    with open(path, "wb") as f:
        f.write(base64.b64decode(final_screenshot))
    logger.info(f"🤖 Final screenshot saved to {path}")

    gif_path = _extracted_from_do_command_23("gifs", result, '.gif')
    create_run_gif(result, gif_path, duration=1500)
    logger.info(f"🤖 GIF saved to {gif_path}")


# TODO Rename this here and in `do_command`
def _extracted_from_do_command_23(arg0, result, arg2):
    folder_path = Path(__file__).parent.parent.parent / arg0
    folder_path.mkdir(parents=True, exist_ok=True)
    result = folder_path / f"{result.run_id}{arg2}"
    return result


def main():
    parser = argparse.ArgumentParser(description="Proxy-Lite")
    parser.add_argument(
        "task",
        type=str,
        help="The task you want to accomplish",
        nargs="*",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="The model to use.",
    )
    parser.add_argument(
        "--api_base",
        type=str,
        default=None,
        help="The API base URL to use.",
    )
    # New option for setting a homepage URL:
    parser.add_argument(
        "--homepage",
        type=str,
        default=None,
        help="The homepage URL to use.",
    )
    # New viewport controls:
    parser.add_argument(
        "--viewport-width",
        type=int,
        default=None,
        help="Viewport width in pixels.",
    )
    parser.add_argument(
        "--viewport-height",
        type=int,
        default=None,
        help="Viewport height in pixels.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).parent / "configs/default.yaml",
        help="Path to config file (default: configs/default.yaml)",
    )

    args = parser.parse_args()
    do_command(args)


if __name__ == "__main__":
    main()
