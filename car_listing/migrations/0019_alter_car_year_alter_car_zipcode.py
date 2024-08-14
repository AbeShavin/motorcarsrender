# Generated by Django 5.0.6 on 2024-08-05 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("car_listing", "0018_alter_car_latitude_alter_car_longitude_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="car",
            name="year",
            field=models.PositiveIntegerField(
                choices=[
                    ("1900", "1900"),
                    ("1910", "1910"),
                    ("1920", "1920"),
                    ("1930", "1930"),
                    ("1940", "1940"),
                    ("1950", "1950"),
                    ("1960", "1960"),
                    ("1970", "1970"),
                    ("1980", "1980"),
                    ("1990", "1990"),
                    ("1991", "1991"),
                    ("1992", "1992"),
                    ("1993", "1993"),
                    ("1994", "1994"),
                    ("1995", "1995"),
                    ("1996", "1996"),
                    ("1997", "1997"),
                    ("1998", "1998"),
                    ("1999", "1999"),
                    ("2000", "2000"),
                    ("2001", "2001"),
                    ("2002", "2002"),
                    ("2003", "2003"),
                    ("2004", "2004"),
                    ("2005", "2005"),
                    ("2006", "2006"),
                    ("2007", "2007"),
                    ("2008", "2008"),
                    ("2009", "2009"),
                    ("2010", "2010"),
                    ("2011", "2011"),
                    ("2012", "2012"),
                    ("2013", "2013"),
                    ("2014", "2014"),
                    ("2015", "2015"),
                    ("2016", "2016"),
                    ("2017", "2017"),
                    ("2018", "2018"),
                    ("2019", "2019"),
                    ("2020", "2020"),
                    ("2021", "2021"),
                    ("2022", "2022"),
                    ("2023", "2023"),
                    ("2024", "2024"),
                    ("2025", "2025"),
                ],
                max_length=4,
            ),
        ),
        migrations.AlterField(
            model_name="car",
            name="zipcode",
            field=models.PositiveIntegerField(default="00000", max_length=5),
        ),
    ]
