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
            id="id", name="test accuracy type in db base name 1"
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

#
def test_cpu_base():
    cpu_base = schemas.cpu.CpuBase(
        name="test cpu name", number_of_cores=2, frequency=3, fp32_per_cycle=7,
        transistors=8, tdp=9.101, gflops=1.121, year=2014, die_size=3
    )

    assert cpu_base.name == "test cpu name"
    assert cpu_base.number_of_cores == 2
    assert cpu_base.frequency == 3
    assert cpu_base.fp32_per_cycle == 7 
    assert cpu_base.transistors == 8
    assert cpu_base.tdp == 9.101 
    assert cpu_base.gflops == 1.121
    assert cpu_base.die_size == 3
    assert cpu_base.year == 2014


def test_cpu_update():
    with pytest.raises(ValueError):
        cpu_update = schemas.cpu.CpuUpdate(number_of_cores="number_of_cores")


def test_cpu_in_db_base():
    cpu_in_db_base = schemas.cpu.CpuInDBBase(
        name="test cpu in db base name"
    )

    assert cpu_in_db_base.name == "test cpu in db base name"


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
