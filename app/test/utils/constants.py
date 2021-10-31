from app.settings import settings

'''
Test constants
'''

# ================================
# BEGIN STATUS_CODE CONSTANTS

SUCCESS = 200
NOT_FOUND = 404
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
METHOD_NOT_ALLOWED = 405
SERVER_ERROR = 500

# END STATUS_CODE CONSTANTS
# ================================


# ================================
# BEGIN DATASETS CONSTANTS

DATASETS_BODY = {
    "name": "string",
    "image": "string",
    "description": "string",
    "source": "string",
    "identifier": "string",
}
DATASETS_KEYS = {*DATASETS_BODY, "id"}

# END DATASETS CONSTANTS
# ================================

# ================================
# BEGIN TASK CONSTANTS

TASK = {
    "name": "bar",
    "image": "foo",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed \
                   do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
                   Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris\
                   nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in \
                   reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla \
                   pariatur. Excepteur sint occaecat cupidatat non proident, sunt in \
                   culpa qui officia deserunt mollit anim id est laborum.",
}

TASK_KEYS = {**TASK, "id": 0, "number_of_benchmarks": 0}

NEW_TASK = {
    "name": "foo",
    "image": "bar",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
}

# END TASK CONSTANTS
# ================================

# ================================
# BEGIN ACCURACY CONSTANTS

ACCURACY_BODY = {
    "name": "Foo",
    "description": "foobar",
}
ACCURACY_KEYS = {*ACCURACY_BODY, "id"}

ACCURACY_KEYS_GET = {*ACCURACY_KEYS, "updated_at", "created_at"}

# END ACCURACY CONSTANTS
# ================================

# ================================
# BEGIN CPU CONSTANTS

CPU_BODY = {
    "name": "string",
    "number_of_cores": 0,
    "frequency": 0,
    "fp32_per_cycle": 0,
    "transistors": 0,
    "tdp": 0,
    "gflops": 0,
    "year": 0,
    "die_size": 0,
}

CPU_NEW = {**CPU_BODY, "year": 2020, "transistors": 3333}

CPU_KEYS = {*CPU_BODY, "id"}

# END CPU CONSTANTS
# ================================

# ================================
# BEGIN TPU CONSTANTS

TPU_BODY = {
  "name": "foobar",
  "transistors": 10,
  "tdp": 20,
  "gflops": 5
}

TPU_NEW = {
    "name": "barfoo",
    "transistors": 50,
    "tdp": 21,
    "gflops": 3
}

# END TPU CONSTANTS
# ================================

# ================================
# BEGIN GPU CONSTANTS

GPU_BODY = {
    "name": "GeForce 8300 GS",
    "transistors": 210,
    "tdp": 40,
    "gflops": 14.4
}

GPU_KEYS = {
    *GPU_BODY,
    "id"
}

# END GPU CONSTANTS
# ================================

# ================================
# BEGIN LOGIN CONSTANTS

LOGIN_EXPECTED_JSON = {
    "email": settings.FIRST_SUPERUSER,
    "is_active": True,
    "role": "super_admin",
    "first_name": None,
    "last_name": None,
}

# END LOGIN CONSTANTS
# ================================

# ================================
# BEGIN SUBMISSION CONSTANTS

SUBMISSION_BODY = {
  "title": "foo",
  "link": "bar",
  "code_link": "foobar",
  "publication_date": "2021-09-09",
  "authors": [
    "bar foo"
  ],
  "models": [
    {
      "name": "foo",
      "task": "foofoo",
      "dataset": "foobar",
      "cpu": "bar foo",
      "gpu": "bar bar",
      "tpu": "bar",
      "gflops": 3,
      "multiply_adds": 2,
      "number_of_parameters": 20,
      "training_time": 30,
      "epochs": 5,
      "extra_training_data": True,
      "accuracies": [
        {
          "accuracy_type": "foo",
          "value": 0.1
        }
      ],
      "number_of_gpus": 3,
      "number_of_cpus": 1,
      "number_of_tpus": 2,
      "extra_training_time": False
    }
  ]
}

SUBMISSION_NEW = {
  "title": "foo",
  "link": "bar",
  "code_link": "foobar",
  "publication_date": "2021-09-09",
  "authors": [
    "bar foo"
  ],
  "models": [
    {
      "name": "foo",
      "task": "foofoo",
      "dataset": "foobar",
      "cpu": "bar foo",
      "gpu": "bar bar",
      "tpu": "bar",
      "gflops": 3,
      "multiply_adds": 2,
      "number_of_parameters": 20,
      "training_time": 30,
      "epochs": 5,
      "extra_training_data": True,
      "accuracies": [
        {
          "accuracy_type": "foo",
          "value": 0.1
        }
      ],
      "number_of_gpus": 3,
      "number_of_cpus": 1,
      "number_of_tpus": 2,
      "extra_training_time": False
    }
  ]
}

SUBMISSION_ALT_BODY = {
  "title": "string",
  "link": "string",
  "code_link": "string",
  "publication_date": "2021-10-30",
  "authors": [
    "string"
  ],
  "models": [
    {
      "name": "string",
      "task": "Image Classification",
      "dataset": "Imagenet",
      "cpu": CPU_BODY["name"],
      "gpu": GPU_BODY["name"],
      "tpu": TPU_BODY["name"],
      "gflops": 0,
      "multiply_adds": 0,
      "number_of_parameters": 0,
      "training_time": 0,
      "epochs": 0,
      "extra_training_data": False,
      "accuracies": [
        {
          "accuracy_type": "TOP 1",
          "value": 1
        }
      ],
      "number_of_gpus": 0,
      "number_of_cpus": 0,
      "number_of_tpus": 0,
      "extra_training_time": False
    }
  ]
}

SUBMISSION_KEYS = {
                  "data": {**SUBMISSION_BODY},
                  "paper_id": 0,
                  "owner_id": 0,
                  "reviewer_id": 0,
                  "status": "pending",
                  "id": 0,
                  "created_at": "2021-09-09T23:17:57.529Z",
                  "updated_at": "2021-09-09T23:17:57.529Z"
                  }

SUBMISSION_MSG_RES = {
  "body": "test foo bar",
  "id": 0,
  "author_id": 0,
  "submission_id": 0,
  "author": {
    "email": "user@example.com",
    "is_active": True,
    "role": "default",
    "first_name": "string",
    "last_name": "string",
    "id": 0
  },
  "type": "string"
}

# END SUBMISSION CONSTANTS
# ================================

# ================================
# BEGIN USER CONSTANTS

USER_BODY = {
    "email": "barbar@foofoo.com",
    "first_name": "Foo",
    "last_name": "bar",
    "password": "foobar",
}

USER_BODY_AUTH = {
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "password": "string",
    }

USER_SUPERUSER_BODY = {
    "email": settings.FIRST_SUPERUSER,
    "role": "super_admin",
    }

USER_KEYS = {
    "email",
    "is_active",
    "role",
    "first_name",
    "last_name",
    "id"
    }

USER_NEW = {
    "email": USER_BODY["email"],
    "first_name": "bazbazbaz",
    "last_name": "foooooo",
}

USER_SUPERUSER_NEW = {
    "email": settings.FIRST_SUPERUSER,
    "first_name": "administrator",
    "last_name": "big boss",
}

# END USER CONSTANTS
# ================================

# ================================
# BEGIN PAPER CONSTANTS

PAPER_GET = {
    "title": "foo",
    "link": "bar",
    "code_link": "baz",
    "publication_date": "2021-10-17",
    "authors": [],
    # "models": []
}

PAPER_BODY = {
    **PAPER_GET,
    "models": []
}

PAPER_KEYS = {*PAPER_GET, "id"}

PAPER_KEYS_POST = {
    *PAPER_KEYS,
    "is_public",
    "updated_at",
    "identifier",
    "link",
    "created_at"
}

PAPER_NEW = {
  **PAPER_GET,
  "title": "foofoo",
  "code_link": "barbar"
}

# END PAPER CONSTANTS
# ================================

# ================================
# BEGIN MODEL CONSTANTS

MODEL_KEYS = {
  "name",
  "hardware_burden",
  "training_time",
  "gflops",
  "epochs",
  "number_of_parameters",
  "multiply_adds",
  "number_of_cpus",
  "number_of_gpus",
  "number_of_tpus",
  "task_dataset_id",
  "task_dataset_id",
  "paper_id",
  "cpu_id",
  "tpu_id",
  "gpu_id",
  "id"
}


# END MODEL CONSTANTS
# ================================
