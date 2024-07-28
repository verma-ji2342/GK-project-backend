from django.db import models


# Create your models here.


class Department(models.Model):
    """
    Dept table
    """

    dept_name = models.CharField(max_length=35)

    def __str__(self):
        return f"Department Name - {self.dept_name}"


class State(models.Model):
    """ "
    State Tables
    """

    state = models.CharField(max_length=40)

    def __str__(self):
        return f"State Name - {self.state}"


class Project(models.Model):
    """
    About Project description
    """

    name = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    

    def __str__(self):
        return f"Project - {self.name}"


class Person(models.Model):
    """
    Person class
    """

    email = models.EmailField(max_length=50)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    pincode = models.PositiveIntegerField()
    address = models.CharField(max_length=100)
    state = models.ForeignKey(
        State,
        related_name="child_two",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    department = models.ForeignKey(
        Department,
        related_name="child_ones",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    project = models.ManyToManyField(Project, related_name="child_three")

    def __str__(self):
        return f"Person - {self.name}"



class Account(models.Model):
    """
    About Salary
    """

    person = models.OneToOneField(
        Person, on_delete=models.CASCADE, related_name="Account", unique=True
    )
    balance = models.PositiveSmallIntegerField()
    DoJ = models.DateField()

    def __str__(self):
        return self.person.name
    
    
