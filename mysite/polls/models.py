from django.db import models

class Student(models.Model):
    id = models.AutoField(primary_key=True)  
    first_name = models.CharField(max_length=30, verbose_name=("Имя"))
    last_name = models.CharField(max_length=30, verbose_name=("Фамилия"))
    date_of_birth = models.DateField(verbose_name=("Дата рождения"))
    enrollment_date = models.DateField(verbose_name=("Дата зачисления"))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Teacher(models.Model):
    id = models.AutoField(primary_key=True)  
    first_name = models.CharField(max_length=30, verbose_name=("Имя"))
    last_name = models.CharField(max_length=30, verbose_name=("Фамилия"))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Subject(models.Model):
    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=50, verbose_name=("Название"))
    code = models.CharField(max_length=10, verbose_name=("Код"))

    def __str__(self):
        return self.name

class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name=("Студент"))
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=("Предмет"))
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name=("Учитель"))
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=("Оценка"))
    date_recorded = models.DateField(verbose_name=("Дата записи"))

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.score}"
