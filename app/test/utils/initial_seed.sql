
insert into "task" ("created_at", "description", "id", "identifier", "image", "name", "updated_at") values ('2021-07-02 02:08:29.864713', 'Image Classification is a fundamental task that attempts to comprehend an entire image as a whole. The goal is to classify the image by assigning it to a specific label. Typically, Image Classification refers to images in which only one object appears and is analyzed. In contrast, object detection involves both classification and localization tasks, and is used to analyze.', 10, 'image-classification', 'https://computerprogress.xyz/image/image-classification.svg', 'Image Classification', '2021-07-02 02:08:29.864713');
insert into "task" ("created_at", "description", "id", "identifier", "image", "name", "updated_at") values ('2021-07-02 02:08:30.399504', 'Named entity recognition (NER) is the task of tagging entities in text with their corresponding type. Approaches typically use BIO notation, which differentiates the beginning (B) and the inside (I) of entities. O is used for non-entity tokens.', 20, 'named-entity-recognition', 'https://computerprogress.xyz/image/named-entity-recognition.svg', 'Named Entity Recognition', '2021-07-02 02:08:30.399504');
insert into "task" ("created_at", "description", "id", "identifier", "image", "name", "updated_at") values ('2021-07-02 02:08:30.547009', 'Object detection is the task of detecting instances of objects of a certain class within an image. The state-of-the-art methods can be categorized into two main types: one-stage methods and two stage-methods. One-stage methods prioritize inference speed, and example models include YOLO, SSD and RetinaNet. Two-stage methods prioritize detection accuracy, and example models include Faster R-CNN, Mask R-CNN and Cascade R-CNN. The most popular benchmark is the MSCOCO dataset. Models are typically evaluated according to a Mean Average Precision metric.', 30, 'object-detection', 'https://computerprogress.xyz/image/object-detection.svg', 'Object Detection', '2021-07-02 02:08:30.547009');
insert into "task" ("created_at", "description", "id", "identifier", "image", "name", "updated_at") values ('2021-07-02 02:08:30.971315', 'Question Answering is the task of answering questions (typically reading comprehension questions), but abstaining when presented with a question that cannot be answered based on the provided context.', 40, 'question-answering', 'https://computerprogress.xyz/image/question-answering.svg', 'Question Answering', '2021-07-02 02:08:30.971315');
insert into "task" ("created_at", "description", "id", "identifier", "image", "name", "updated_at") values ('2021-07-02 02:08:31.147218', 'Machine translation is the task of translating a sentence in a source language to a different target language.', 50, 'machine-translation', 'https://computerprogress.xyz/image/machine-translation.svg', 'Machine Translation', '2021-07-02 02:08:31.147218');

insert into "dataset" ("created_at", "description", "id", "identifier", "image", "name", "source", "updated_at") values ('2021-07-02 02:08:29.864713', NULL, 10, 'imagenet', NULL, 'Imagenet', NULL, '2021-07-02 02:08:29.864713');
insert into "dataset" ("created_at", "description", "id", "identifier", "image", "name", "source", "updated_at") values ('2021-07-02 02:08:30.399504', NULL, 20, 'conll-2003', NULL, 'Conll 2003', NULL, '2021-07-02 02:08:30.399504');
insert into "dataset" ("created_at", "description", "id", "identifier", "image", "name", "source", "updated_at") values ('2021-07-02 02:08:30.547009', NULL, 30, 'ms-coco', NULL, 'MS COCO', NULL, '2021-07-02 02:08:30.547009');
insert into "dataset" ("created_at", "description", "id", "identifier", "image", "name", "source", "updated_at") values ('2021-07-02 02:08:30.971315', NULL, 40, 'squad11', NULL, 'SQuAD 1.1', NULL, '2021-07-02 02:08:30.971315');
insert into "dataset" ("created_at", "description", "id", "identifier", "image", "name", "source", "updated_at") values ('2021-07-02 02:08:31.147218', NULL, 50, 'wmt2014-en-ge', NULL, 'WMT2014 English-German', NULL, '2021-07-02 02:08:31.147218');
insert into "dataset" ("created_at", "description", "id", "identifier", "image", "name", "source", "updated_at") values ('2021-07-02 02:08:31.312437', NULL, 60, 'wmt2014-en-fr', NULL, 'WMT2014 English-French', NULL, '2021-07-02 02:08:31.312437');

insert into "accuracy_type" ("created_at", "description", "id", "name", "updated_at") values ('2021-07-02 02:08:29.864713', NULL, 10, 'TOP 1', '2021-07-02 02:08:29.864713');
insert into "accuracy_type" ("created_at", "description", "id", "name", "updated_at") values ('2021-07-02 02:08:29.864713', NULL, 20, 'TOP 5', '2021-07-02 02:08:29.864713');
insert into "accuracy_type" ("created_at", "description", "id", "name", "updated_at") values ('2021-07-02 02:08:30.399504', NULL, 30, 'F1', '2021-07-02 02:08:30.399504');
insert into "accuracy_type" ("created_at", "description", "id", "name", "updated_at") values ('2021-07-02 02:08:30.547009', NULL, 40, 'BOX AP', '2021-07-02 02:08:30.547009');
insert into "accuracy_type" ("created_at", "description", "id", "name", "updated_at") values ('2021-07-02 02:08:30.547009', NULL, 50, 'AP50', '2021-07-02 02:08:30.547009');
insert into "accuracy_type" ("created_at", "description", "id", "name", "updated_at") values ('2021-07-02 02:08:30.547009', NULL, 60, 'AP75', '2021-07-02 02:08:30.547009');
insert into "accuracy_type" ("created_at", "description", "id", "name", "updated_at") values ('2021-07-02 02:08:30.547009', NULL, 70, 'APS', '2021-07-02 02:08:30.547009');
insert into "accuracy_type" ("created_at", "description", "id", "name", "updated_at") values ('2021-07-02 02:08:30.547009', NULL, 80, 'APM', '2021-07-02 02:08:30.547009');
insert into "accuracy_type" ("created_at", "description", "id", "name", "updated_at") values ('2021-07-02 02:08:30.547009', NULL, 90, 'APL', '2021-07-02 02:08:30.547009');
insert into "accuracy_type" ("created_at", "description", "id", "name", "updated_at") values ('2021-07-02 02:08:30.971315', NULL, 100, 'F1', '2021-07-02 02:08:30.971315');
insert into "accuracy_type" ("created_at", "description", "id", "name", "updated_at") values ('2021-07-02 02:08:30.971315', NULL, 101, 'EM', '2021-07-02 02:08:30.971315');
insert into "accuracy_type" ("created_at", "description", "id", "name", "updated_at") values ('2021-07-02 02:08:31.147218', NULL, 102, 'BLEU score', '2021-07-02 02:08:31.147218');
insert into "accuracy_type" ("created_at", "description", "id", "name", "updated_at") values ('2021-07-02 02:08:31.147218', NULL, 103, 'SacreBLEU', '2021-07-02 02:08:31.147218');
insert into "accuracy_type" ("created_at", "description", "id", "name", "updated_at") values ('2021-07-02 02:08:31.312437', NULL, 104, 'BLEU score', '2021-07-02 02:08:31.312437');
insert into "accuracy_type" ("created_at", "description", "id", "name", "updated_at") values ('2021-07-02 02:08:31.312437', NULL, 105, 'SacreBLEU', '2021-07-02 02:08:31.312437');

insert into "task_dataset" ("created_at", "dataset_id", "id", "identifier", "task_id", "updated_at") values ('2021-07-02 02:08:29.864713', 10, 10, 'image-classification-on-imagenet', 10, '2021-07-02 02:08:29.864713');
insert into "task_dataset" ("created_at", "dataset_id", "id", "identifier", "task_id", "updated_at") values ('2021-07-02 02:08:30.399504', 20, 20, 'named-entity-recognition-on-conll-2003', 20, '2021-07-02 02:08:30.399504');
insert into "task_dataset" ("created_at", "dataset_id", "id", "identifier", "task_id", "updated_at") values ('2021-07-02 02:08:30.547009', 30, 30, 'object-detection-on-ms-coco', 30, '2021-07-02 02:08:30.547009');
insert into "task_dataset" ("created_at", "dataset_id", "id", "identifier", "task_id", "updated_at") values ('2021-07-02 02:08:30.971315', 40, 40, 'question-answering-on-squad11', 40, '2021-07-02 02:08:30.971315');
insert into "task_dataset" ("created_at", "dataset_id", "id", "identifier", "task_id", "updated_at") values ('2021-07-02 02:08:31.147218', 50, 50, 'machine-translation-on-wmt2014-en-ge', 50, '2021-07-02 02:08:31.147218');
insert into "task_dataset" ("created_at", "dataset_id", "id", "identifier", "task_id", "updated_at") values ('2021-07-02 02:08:31.312437', 60, 60, 'machine-translation-on-wmt2014-en-fr', 50, '2021-07-02 02:08:31.312437');

insert into "task_dataset_accuracy_type" ("accuracy_type_id", "created_at", "id", "main", "required", "task_dataset_id", "updated_at") values (10, '2021-07-02 02:08:29.864713', 10, true, true, 10, '2021-07-02 02:08:29.864713');
insert into "task_dataset_accuracy_type" ("accuracy_type_id", "created_at", "id", "main", "required", "task_dataset_id", "updated_at") values (20, '2021-07-02 02:08:29.864713', 20, false, false, 10, '2021-07-02 02:08:29.864713');
insert into "task_dataset_accuracy_type" ("accuracy_type_id", "created_at", "id", "main", "required", "task_dataset_id", "updated_at") values (30, '2021-07-02 02:08:30.399504', 30, true, true, 20, '2021-07-02 02:08:30.399504');
insert into "task_dataset_accuracy_type" ("accuracy_type_id", "created_at", "id", "main", "required", "task_dataset_id", "updated_at") values (40, '2021-07-02 02:08:30.547009', 40, true, true, 30, '2021-07-02 02:08:30.547009');
insert into "task_dataset_accuracy_type" ("accuracy_type_id", "created_at", "id", "main", "required", "task_dataset_id", "updated_at") values (50, '2021-07-02 02:08:30.547009', 50, false, false, 30, '2021-07-02 02:08:30.547009');
insert into "task_dataset_accuracy_type" ("accuracy_type_id", "created_at", "id", "main", "required", "task_dataset_id", "updated_at") values (60, '2021-07-02 02:08:30.547009', 60, false, false, 30, '2021-07-02 02:08:30.547009');
insert into "task_dataset_accuracy_type" ("accuracy_type_id", "created_at", "id", "main", "required", "task_dataset_id", "updated_at") values (70, '2021-07-02 02:08:30.547009', 70, false, false, 30, '2021-07-02 02:08:30.547009');
insert into "task_dataset_accuracy_type" ("accuracy_type_id", "created_at", "id", "main", "required", "task_dataset_id", "updated_at") values (80, '2021-07-02 02:08:30.547009', 80, false, false, 30, '2021-07-02 02:08:30.547009');
insert into "task_dataset_accuracy_type" ("accuracy_type_id", "created_at", "id", "main", "required", "task_dataset_id", "updated_at") values (90, '2021-07-02 02:08:30.547009', 90, false, false, 30, '2021-07-02 02:08:30.547009');
insert into "task_dataset_accuracy_type" ("accuracy_type_id", "created_at", "id", "main", "required", "task_dataset_id", "updated_at") values (100, '2021-07-02 02:08:30.971315', 100, true, true, 40, '2021-07-02 02:08:30.971315');
insert into "task_dataset_accuracy_type" ("accuracy_type_id", "created_at", "id", "main", "required", "task_dataset_id", "updated_at") values (101, '2021-07-02 02:08:30.971315', 101, false, false, 40, '2021-07-02 02:08:30.971315');
insert into "task_dataset_accuracy_type" ("accuracy_type_id", "created_at", "id", "main", "required", "task_dataset_id", "updated_at") values (102, '2021-07-02 02:08:31.147218', 102, true, true, 50, '2021-07-02 02:08:31.147218');
insert into "task_dataset_accuracy_type" ("accuracy_type_id", "created_at", "id", "main", "required", "task_dataset_id", "updated_at") values (103, '2021-07-02 02:08:31.147218', 103, false, false, 50, '2021-07-02 02:08:31.147218');
insert into "task_dataset_accuracy_type" ("accuracy_type_id", "created_at", "id", "main", "required", "task_dataset_id", "updated_at") values (104, '2021-07-02 02:08:31.312437', 104, true, true, 60, '2021-07-02 02:08:31.312437');
insert into "task_dataset_accuracy_type" ("accuracy_type_id", "created_at", "id", "main", "required", "task_dataset_id", "updated_at") values (105, '2021-07-02 02:08:31.312437', 105, false, false, 60, '2021-07-02 02:08:31.312437');
