from app import schemas

import pytest


def test_accuracy_type_base_1():
    accuracy_type_base = schemas.accuracy_type.AccuracyTypeBase(
        name="test accuracy type base name 1",
        description="test accuracy type base description 1"
    )

    assert accuracy_type_base.name == "test accuracy type base name 1"
    assert accuracy_type_base.description == "test accuracy type base description 1"


def test_accuracy_type_base_2():
    accuracy_type_base = schemas.accuracy_type.AccuracyTypeBase(
        name="test accuracy type base name 2"
    )

    assert accuracy_type_base.name == "test accuracy type base name 2"


def test_accuracy_type_base_3():
    with pytest.raises(ValueError):
        accuracy_type_base = schemas.accuracy_type.AccuracyTypeBase(
            description="test accuracy type base description 3"
        )


def test_accuracy_type_update1():
    accuracy_type_update = schemas.accuracy_type.AccuracyTypeUpdate(
        name="test accuracy type update name 1",
        description="test accuracy type update description 1"
    )

    assert accuracy_type_update.name == "test accuracy type update name 1"
    assert accuracy_type_update.description == "test accuracy type update description 1"


def test_accuracy_type_update2():
    accuracy_type_update = schemas.accuracy_type.AccuracyTypeUpdate(
        name="test accuracy type update name 2"
    )

    assert accuracy_type_update.name == "test accuracy type update name 2"


def test_accuracy_type_in_db_base1():
    with pytest.raises(ValueError):
        accuracy_type_in_db_base = schemas.accuracy_type.AccuracyTypeInDBBase(
            id="id_accuracy_type_in_db_base", name="test accuracy type in db base name 1"
        )


def test_accuracy_type_in_db_base2():
    with pytest.raises(ValueError):
        accuracy_type_in_db_base = schemas.accuracy_type.AccuracyTypeInDBBase(id=1)


def test_accuracy_type_in_db_base3():
    accuracy_type_in_db_base = schemas.accuracy_type.AccuracyTypeInDBBase(
        name="test accuracy type in db base name 3",
        description="test accuracy type in db base description 3"
    )

    assert accuracy_type_in_db_base.name == "test accuracy type in db base name 3"
    assert accuracy_type_in_db_base.description == "test accuracy type in db base description 3"


def test_accuracy_type_in_db_base4():
    accuracy_type_in_db_base = schemas.accuracy_type.AccuracyTypeInDBBase(
        id=2, name="test accuracy type in db base name 4",
        description="test accuracy type in db base description 4",
    )

    assert accuracy_type_in_db_base.id == 2
    assert accuracy_type_in_db_base.name == "test accuracy type in db base name 4"
    assert accuracy_type_in_db_base.description == "test accuracy type in db base description 4"


def test_cpu_base1():
    cpu_base = schemas.cpu.CpuBase(
        name="test cpu base name 1", number_of_cores=2, frequency=3, fp32_per_cycle=7,
        transistors=8, tdp=9.101, gflops=1.121, year=2014, die_size=3
    )

    assert cpu_base.name == "test cpu base name 1"
    assert cpu_base.number_of_cores == 2
    assert cpu_base.frequency == 3
    assert cpu_base.fp32_per_cycle == 7
    assert cpu_base.transistors == 8
    assert cpu_base.tdp == 9.101
    assert cpu_base.gflops == 1.121
    assert cpu_base.year == 2014
    assert cpu_base.die_size == 3


def test_cpu_base2():
    cpu_base = schemas.cpu.CpuBase(
        name="test cpu base name 2"
    )

    assert cpu_base.name == "test cpu base name 2"


def test_cpu_base3():
    with pytest.raises(ValueError):
        cpu_base = schemas.cpu.CpuBase(
            number_of_cores=3, frequency=4, fp32_per_cycle=8,
            transistors=9, tdp=10.101, gflops=11.121, year=2015, die_size=4
        )


def test_cpu_base4():
    with pytest.raises(ValueError):
        cpu_base = schemas.cpu.CpuBase(
            name="test cpu base name 4", number_of_cores="number_of_cores_cpu_base_4", frequency=5,
            fp32_per_cycle=9, transistors=10, tdp=11.101, gflops=12.121, year=2016, die_size=5
        )   


def test_cpu_update1():
    cpu_update = schemas.cpu.CpuUpdate(
        name="test cpu update name 1", number_of_cores=6, frequency=6, fp32_per_cycle=10,
        transistors=11, tdp=12.101, gflops=13.121, year=2017, die_size=6
    )

    assert cpu_update.name == "test cpu update name 1"
    assert cpu_update.number_of_cores == 6
    assert cpu_update.frequency == 6
    assert cpu_update.fp32_per_cycle == 10
    assert cpu_update.transistors == 11
    assert cpu_update.tdp == 12.101
    assert cpu_update.gflops == 13.121
    assert cpu_update.year == 2017
    assert cpu_update.die_size == 6


def test_cpu_update2():
    cpu_update = schemas.cpu.CpuUpdate(
        name="test cpu update name 2", number_of_cores=7, frequency=7, fp32_per_cycle=11,
        transistors=12, tdp=13.101, gflops=14.121, year=2018
    )

    assert cpu_update.name == "test cpu update name 2"
    assert cpu_update.number_of_cores == 7
    assert cpu_update.frequency == 7
    assert cpu_update.fp32_per_cycle == 11
    assert cpu_update.transistors == 12
    assert cpu_update.tdp == 13.101
    assert cpu_update.gflops == 14.121
    assert cpu_update.year == 2018


def test_cpu_update3():
    with pytest.raises(ValueError):
        cpu_update = schemas.cpu.CpuUpdate(
            name="test cpu update name 3", number_of_cores="number_of_cores_cpu_update_3", frequency=8,
            fp32_per_cycle=12, transistors=13, tdp=14.101, gflops=15.121, year=2019, die_size=7
        )


def test_cpu_in_db_base1():
    cpu_in_db_base = schemas.cpu.CpuInDBBase(
        id=3, name="test cpu in db base name 1", number_of_cores=8, frequency=9, fp32_per_cycle=13,
        transistors=14, tdp=15.101, gflops=16.121, year=2020, die_size=8
    )

    assert cpu_in_db_base.id == 3
    assert cpu_in_db_base.name == "test cpu in db base name 1"
    assert cpu_in_db_base.number_of_cores == 8
    assert cpu_in_db_base.frequency == 9
    assert cpu_in_db_base.fp32_per_cycle == 13
    assert cpu_in_db_base.transistors == 14
    assert cpu_in_db_base.tdp == 15.101
    assert cpu_in_db_base.gflops == 16.121
    assert cpu_in_db_base.year == 2020
    assert cpu_in_db_base.die_size == 8


def test_cpu_in_db_base2():
    cpu_in_db_base = schemas.cpu.CpuInDBBase(
        name="test cpu in db base name 2", number_of_cores=9, frequency=10, fp32_per_cycle=14,
        transistors=15, tdp=16.101, gflops=17.121, die_size=9
    )

    assert cpu_in_db_base.name == "test cpu in db base name 2"
    assert cpu_in_db_base.number_of_cores == 9
    assert cpu_in_db_base.frequency == 10
    assert cpu_in_db_base.fp32_per_cycle == 14
    assert cpu_in_db_base.transistors == 15
    assert cpu_in_db_base.tdp == 16.101
    assert cpu_in_db_base.gflops == 17.121
    assert cpu_in_db_base.die_size == 9


def test_cpu_in_db_base3():
    with pytest.raises(ValueError):
       cpu_in_db_base = schemas.cpu.CpuInDBBase(
            number_of_cores=10, frequency=11, fp32_per_cycle=15, transistors=16, tdp=17.101, 
            gflops=18.121, die_size=19
        )


def test_cpu_in_db_base4():
    with pytest.raises(ValueError):
       cpu_in_db_base = schemas.cpu.CpuInDBBase(
            id="id_cpu_in_db_base_4", number_of_cores=11, frequency=12, fp32_per_cycle=16, transistors=17,
            tdp=18.101, gflops=19.121, die_size=20
        )


def test_dataset_base():
    dataset_base = schemas.dataset.DatasetBase(
        name="test dataset base name", image="test dataset base string image",
        description="test dataset base description", source="test dataset base source",
        identifier="test dataset base identifier"
    )

    assert dataset_base.name == "test dataset base name"
    assert dataset_base.image == "test dataset base string image"
    assert dataset_base.description == "test dataset base description"
    assert dataset_base.source == "test dataset base source"
    assert dataset_base.identifier == "test dataset base identifier"


def test_dataset_update():
    dataset_update = schemas.dataset.DatasetUpdate(
        name="test dataset base name update", image="test dataset base string image",
        description="test dataset base description", source="test dataset base source",
        identifier="test dataset base identifier"
    )

    assert dataset_update.name == "test dataset base name update"
    assert dataset_update.image == "test dataset base string image"
    assert dataset_update.description == "test dataset base description"
    assert dataset_update.source == "test dataset base source"
    assert dataset_update.identifier == "test dataset base identifier"


def test_dataset_in_db_base():
    with pytest.raises(ValueError):
        dataset_in_db_base = schemas.dataset.DatasetInDBBase(id="id")
