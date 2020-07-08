import time

import win32pdh

try:
    import obspython as obs
except ImportError:
    obs = None

GAMES = {"ModernWarfare"}


def is_game_running():
    """
    Return whether we are currently running a game.
    """
    _, instances = win32pdh.EnumObjectItems(
        None, None, "Process", win32pdh.PERF_DETAIL_WIZARD)
    return not GAMES.isdisjoint(instances)


def timer():
    """
    Timer to look for the presence of games and start/stop recording as necessary.
    """
    start = time.time()
    running = is_game_running()
    end = time.time()
    duration = end - start
    print(f"is_game_running(): {running}")
    print(f"duration: {duration}")


def script_update(settings):
    """
    Initialise the timer.
    """
    timer()
    interval = obs.obs_data_get_int(settings, "interval")
    obs.timer_remove(timer)
    obs.timer_add(timer, interval * 1000)


def script_description():
    """
    Define the script description.
    """
    return "Automates starting and stopping OBS recording according to which games are running"


def script_defaults(settings):
    obs.obs_data_set_default_int(settings, "interval", 10)


def script_properties():
    """
    Define the configuration properties for the script.
    """
    props = obs.obs_properties_create()

    p = obs.obs_properties_add_list(props, "executables", "Game executable",
                                    obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)

    obs.obs_properties_add_int(
        props, "interval", "Game scan interval (seconds)", 1, 60, 1)

    return props


if __name__ == "__main__":
    timer()
