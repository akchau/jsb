from core.poller.poller_client import BasePollerWithParams

from ..number_request_controller import reset_lost_trying


class ResetPoller(BasePollerWithParams):

    def process_polling(self):
        self.reset_if_time_to_reset()

    def is_time_to_reset(self):
        return self.memory.get_last_time_update()

    def reset_if_time_to_reset(self):
        if self.is_time_to_reset():
            reset_lost_trying()


def start_reset_poller():
    ResetPoller(
        poll_interval=300,
        thread_name="reset_poller",
    ).start_polling()
