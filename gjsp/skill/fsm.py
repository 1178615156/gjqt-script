import logging


class FSM:
    def __init__(self):
        self.__init_status = None
        self.__status_history = []
        self.__current_status = None
        self.__status_action = {}
        self.__transform = {}

    def logger(self): return logging.getLogger("fsm")

    def status_action(self): return self.__status_action

    def current_status(self): return self.__current_status

    def transform(self): return self.__transform

    def init_status(self, status):
        self.__init_status = status
        self.__current_status = status

    def clear(self):
        self.init_status(self.__init_status)

    def add_action(self, status, action):
        self.status_action()[status] = action

    def add_transform(self, from_, to_, action):
        self.transform()[(from_, to_)] = action

    def become(self, new_status):
        self.__status_history.append(self.current_status())
        self.__current_status = new_status

    def un_become(self):
        self.__current_status = self.__status_history[-1]
        self.__status_history = self.__status_history[:-1]

    def run(self):
        action = self.status_action().get(self.current_status())
        assert action is not None, "have not init status"
        old_status = self.current_status()
        action()
        new_status = self.current_status()
        if old_status is not new_status:
            self.logger().info("become %s -> %s " % (str(old_status), str(new_status)))
            transform = self.transform().get((old_status, new_status), lambda: ())
            transform()

