from unittest import TestCase
from gjsp.skill.fsm import FSM

Hello = "Hello"
World = "World"


class _MyFSMTest(FSM):
    def __init__(self):
        super().__init__()

        self.init_status(Hello)
        self.add_action(Hello, self.say_hello)
        self.add_action(World, self.say_world)
        self.add_transform(Hello, World, self.hello_to_world)

    def say_hello(self):
        print("hello")
        self.become(World)

    def say_world(self):
        print("world")
        self.become(World)

    def hello_to_world(self):
        print("hello to world")


class TestFSM(TestCase):
    def test_fsm(self):
        print("-----------------------")
        fsm = _MyFSMTest()
        fsm.run()
        fsm.run()
        fsm.run()
