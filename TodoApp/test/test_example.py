import pytest


def test_equal_or_not_equal():
    assert 3 == 3
    assert "Hello" == "Hello"



class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def student():
    return Student("John", "Doe", "Mathematics", 3)


def test_person(student):
    assert student.first_name == "John", "First name should be John"
    assert student.last_name == "Doe", "Last name should be Doe"
    assert student.major == "Mathematics"
    assert student.years == 3