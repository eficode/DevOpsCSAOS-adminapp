from ast import excepthandler
from os import getenv
import unittest
import uuid
from datetime import datetime, timedelta

from repositories.survey_repository import SurveyRepository

from app import create_app

text = "create question test"
category_weights = '[{"category": "Category 1", "multiplier": 10.0}, {"category": "Category 2", "multiplier": 20.0}]'


class TestSurveyRepository(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.repo = SurveyRepository()

    def tearDown(self):
        self.app.db.get_engine(self.app).dispose()

    def test_authorized_google_login_with_valid_email_succeeds(self):

        valid_email = getenv('ADMIN_EMAIL_1')

        with self.app.app_context():
            response = self.repo.authorized_google_login(valid_email)

        self.assertTrue(response)

    def test_authorized_google_login_with_invalid_email_fails(self):

        valid_email = "test@gmail.invalid"

        with self.app.app_context():
            response = self.repo.authorized_google_login(valid_email)

        self.assertFalse(response)

    def test_create_survey_with_valid_data_returns_id(self):

        with self.app.app_context():
            response = self.repo.create_survey(
                "name",
                "title",
                "text")

        self.assertGreater(response, 0)

    def test_create_survey_with_invalid_data_returns_none(self):

        with self.app.app_context():
            response = self.repo.create_survey(
                None,
                "title",
                "text")

        self.assertIsNone(response)

    def test_survey_with_the_same_name_exists(self):
        with self.app.app_context():
            self.repo.create_survey(
                "MDZS",
                "Rejoice!",
                "WWX is dead!"
            )
            response = self.repo.survey_exists("mdzs")

            self.assertTrue(response)

    def test_survey_with_the_same_name_doesnt_exist(self):
        with self.app.app_context():
            response = self.repo.survey_exists("totally nonexistent survey")
        self.assertFalse(response[0])

    def test_get_survey_with_valid_id_returns_survey(self):

        with self.app.app_context():
            response = self.repo.get_survey(1)

        self.assertIsNotNone(response)

    def test_get_survey_with_invalid_id_returns_false(self):

        with self.app.app_context():
            response = self.repo.get_survey(999999)

        self.assertFalse(response)

    def test_get_survey_id_from_question_id_returns_correct_value(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "Algorithms", "Sorting algorithms", "Have fun with sorting!")
            question_id = self.repo.create_question(
                "In which situations can a bubble sorting algorithm be useful?", survey_id, category_weights)
            received_id = self.repo.get_survey_id_from_question_id(question_id)
        self.assertTrue(received_id == survey_id)

    def test_get_question_id_from_answer_id_returns_correct_value(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "Data structures", "Storing information", "Have fun with storing!")
            question_id = self.repo.create_question(
                "What are the drawbacks of hashmaps?", survey_id, category_weights)
            answer_id = self.repo.create_answer(
                text="Slow lookup times when looking by key", points=-10, question_id=question_id)
            received_id = self.repo.get_question_id_from_answer_id(answer_id)
        self.assertTrue(received_id == question_id)

    def test_update_survey_updated_at_changes_updated_field(self):
        with self.app.app_context():
            before = self.repo.get_survey(1)[3]
            self.repo.update_survey_updated_at(1)
            after = self.repo.get_survey(1)[3]
        self.assertGreater(after, before)

    def test_delete_question_answer_updates_survey_updated_at(self):
        with self.app.app_context():
            question_id = self.repo.create_question(
                "What brings you comfort?", 1, category_weights)
            answer_id = self.repo.create_answer("Unit tests", question_id, 5)
            before = self.repo.get_survey(1)[3]
            self.repo.delete_answer_from_question(answer_id)
            after = self.repo.get_survey(1)[3]
        self.assertGreater(after, before)

    def test_delete_question_updates_survey_updated_at(self):
        with self.app.app_context():
            question_id = self.repo.create_question(
                "Has my existence made any difference in the end?", 1, category_weights)
            before = self.repo.get_survey(1)[3]
            self.repo.delete_question_from_survey(question_id)
            after = self.repo.get_survey(1)[3]
        self.assertGreater(after, before)

    def test_create_category_updates_survey_updated_at(self):
        content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
        with self.app.app_context():
            before = self.repo.get_survey(1)[3]
            self.repo.create_category(
                "1",
                "name",
                "description",
                content_links)
            after = self.repo.get_survey(1)[3]
            print("After:", after)
        self.assertGreater(after, before)

    def update_category_updates_survey_updated_at(self):
        content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
        with self.app.app_context():
            before = self.repo.get_survey(1)[3]
            self.repo.update_category(
                "1",
                "name",
                "improved description",
                content_links)
            after = self.repo.get_survey(1)[3]
        self.assertGreater(after, before)

    def delete_category_updates_survey_updated_at(self):
        content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
        with self.app.app_context():
            category = self.repo.create_category(
                "1",
                "name",
                "description",
                content_links)
            before = self.repo.get_survey(1)[3]
            self.repo.delete_category(category)
            after = self.repo.get_survey(1)[3]
        self.assertGreater(after, before)

    def survey_updated_at_remains_unaltered_without_changes(self):
        with self.app.app_context():
            before = self.repo.get_survey(1)
            after = self.repo.get_survey(1)
        self.assertEqual(after, before)

    def test_get_all_surveys_with_correct_question_counts(self):

        with self.app.app_context():
            response = self.repo.get_all_surveys()

        first_survey_with_questions = response[0][2]
        self.assertEqual(first_survey_with_questions, 12)
        second_survey_without_questions = response[1][2]
        self.assertEqual(second_survey_without_questions, 0)
        third_survey_with_a_question = response[2][2]
        self.assertEqual(third_survey_with_a_question, 1)

    def test_get_all_surveys_returns_correct_amount_of_surveys(self):

        with self.app.app_context():
            response = self.repo.get_all_surveys()
        self.assertEqual(len(response), 19)

    def test_get_questions_of_survey_returns_questions(self):

        with self.app.app_context():
            response = self.repo.get_questions_of_survey(1)

        self.assertGreater(len(response), 2)

    def test_get_answers_of_question_returns_questions(self):

        with self.app.app_context():
            response = self.repo.get_question_answers(2)
        self.assertGreater(len(response), 0)

    def test_edit_survey_returns_none_with_invalid_arguments(self):

        with self.app.app_context():
            response = self.repo.edit_survey(
                None,
                "name_test",
                "title_test",
                "description_test"
            )

        self.assertIsNone(response)

    def test_edit_survey_returns_id_with_valid_arguments(self):

        with self.app.app_context():
            response = self.repo.edit_survey(
                "1",
                "name_test",
                "title_test",
                "description_test"
            )

        self.assertEqual(response, 1)

    def test_edit_survey_returns_false_with_invalid_input(self):

        with self.app.app_context():
            response = self.repo.edit_survey(
                "one",
                "mame_test",
                "title_test",
                "description_test"
            )

        self.assertFalse(response)

    def test_get_question_with_invalid_id_returns_none(self):

        with self.app.app_context():
            response = self.repo.get_question(99999)

        self.assertIsNone(response)

    def test_delete_survey_deletes_existing_survey(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "Mock survey with little to no content",
                "in test def test_delete_survey_deletes_existing_survey(self):",
                "in survey_repository_test.py")
            self.assertTrue(self.repo.get_survey(survey_id) != False)
            self.repo.delete_survey(survey_id)
            response = self.repo.get_survey(survey_id)
        self.assertFalse(response)

    # TODO: Add functionality to this test as data becomes available.

    def test_delete_survey_deletes_related_data(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "Mock survey with little to no content",
                "in test def test_delete_survey_deletes_existing_survey(self):",
                "in survey_repository_test.py")
            self.assertTrue(self.repo.get_survey(survey_id) != False)
            self.repo.delete_survey(survey_id)
            response = self.repo.get_survey(survey_id)
            get_related_questions = self.repo.get_questions_of_survey(
                survey_id)
            get_related_survey_results = []
        self.assertFalse(response)
        self.assertTrue(len(get_related_questions) == 0)
        self.assertTrue(len(get_related_survey_results) == 0)

    def test_create_question_creates_question(self):

        with self.app.app_context():

            survey_id = 1

            question_id = self.repo.create_question(
                text, survey_id, category_weights)

            result = self.repo.get_question(question_id)

        self.assertEqual(result.text, "create question test")

    def test_delete_question_from_survey_deletes_question(self):

        with self.app.app_context():
            survey_id = 1

            question_id = self.repo.create_question(
                text, survey_id, category_weights)

            response_delete = self.repo.delete_question_from_survey(
                question_id)
            response_get_deleted = self.repo.get_question(question_id)

        self.assertTrue(response_delete)
        self.assertIsNone(response_get_deleted)

    def test_delete_question_from_survey_deletes_question_answers(self):

        with self.app.app_context():
            survey_id = 1

            question_id = self.repo.create_question(
                text, survey_id, category_weights)

            for i in range(10):
                self.repo.create_answer(
                    "Test answer " + str(i), points=i*10, question_id=question_id)
            self.repo.delete_question_from_survey(
                question_id)
            response_get_answers = self.repo.get_question_answers(
                question_id)

        self.assertTrue(len(response_get_answers) == 0)

    def test_get_user_answers_returns_None_when_none_exist(self):

        with self.app.app_context():
            survey_id = 1
            question_id = self.repo.create_question(
                text, survey_id, category_weights)
            result = self.repo.get_user_answers(question_id)
        self.assertIsNone(result)

    def test_get_user_answers_returns_all_answers(self):

        with self.app.app_context():
            survey_id = 1
            question_id = self.repo.create_question(
                text, survey_id, category_weights)
            for i in range(5):
                self.repo.create_answer(
                    "Test answer " + str(i), points=i*10, question_id=question_id)
            answers = self.repo.get_question_answers(question_id)
        self.assertTrue(len(answers) == 5)
        self.assertTrue(
            answers[0][1] == "Test answer 0" and answers[4][1] == "Test answer 4")

    def test_delete_answer_from_question_deletes_answer(self):

        with self.app.app_context():
            text = "Breaking Bad"
            points = 9001
            question_id = 9

            answer_id = self.repo.create_answer(
                text, points, question_id)

            response_delete = self.repo.delete_answer_from_question(
                answer_id)
            response_get_deleted = self.repo.get_question_answers(question_id)

        self.assertTrue(response_delete)
        self.assertEqual(response_get_deleted, [])

    def test_update_question_updates_question(self):

        with self.app.app_context():
            survey_id = 1
            category_weights = '[{"category": "Category 1", "multiplier": 10.0}, {"category": "Category 2", "multiplier": 20.0}]'

            question_id = self.repo.create_question(
                text, survey_id, category_weights)

            new_text = "update question test"

            result_update = self.repo.update_question(
                question_id, new_text, category_weights, [], [])

            result_get_new = self.repo.get_question(question_id)

        self.assertTrue(result_update)
        self.assertEqual(result_get_new.text, "update question test")

    def test_update_question_updates_answers(self):

        with self.app.app_context():
            question_id = 10
            question = self.repo.get_question(question_id)
            original_answers = self.repo.get_question_answers(question_id)
            new_answers = [(original_answers[0][0], "changed", 2),
                           (original_answers[1][0], "muutettu", -2)]
            changed = self.repo.update_question(question_id, question[0], question[3],
                                                original_answers, new_answers)
            changed_answers = self.repo.get_question_answers(question_id)
            self.assertTrue(changed)
            self.assertEqual(new_answers, changed_answers)
            self.repo.update_question(question_id, question[0], question[3],
                                      changed_answers, original_answers)

    def test_create_category_with_valid_data_returns_id(self):
        content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'

        with self.app.app_context():
            response = self.repo.create_category(
                "1",
                "name",
                "description",
                content_links)

        self.assertGreater(response, 0)

    def test_create_category_with_invalid_data_returns_none(self):
        with self.app.app_context():
            response = self.repo.create_category(
                "1",
                None,
                "description",
                "content_links")

        self.assertIsNone(response)

    def test_get_all_categories_returns_multiple_categories(self):
        with self.app.app_context():
            response = self.repo.get_all_categories()

        self.assertGreater(len(response), 2)

    def test_add_admin_with_invalid_data_returns_none(self):

        with self.app.app_context():
            response = self.repo.add_admin(
                {"test": "test"}
            )

        self.assertIsNone(response)

    def test_add_admin_with_valid_data_returns_id(self):

        with self.app.app_context():
            response = self.repo.add_admin("test@email.com")

        self.assertIsNotNone(response)

    def test_get_all_admins_returns_multiple_admins(self):

        with self.app.app_context():
            response = self.repo.get_all_admins()

        self.assertGreater(len(response), 1)

    def test_update_category_with_valid_data_returns_id(self):
        with self.app.app_context():
            categories = self.repo.get_all_categories()
            category_id = categories[0][0]
            content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
            response = self.repo.update_category(
                category_id,
                "name",
                "description",
                content_links)
        self.assertTrue(response != None)
        self.assertGreaterEqual(response, 0)

    def test_update_category_with_invalid_data_returns_False(self):
        with self.app.app_context():
            category_id = -1
            content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
            response = self.repo.update_category(
                category_id,
                "name",
                "description",
                content_links)
        self.assertFalse(response)

        with self.app.app_context():
            category_id = 2.5
            content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
            response = self.repo.update_category(
                category_id,
                "name",
                "description",
                content_links)
        self.assertFalse(response)
        with self.app.app_context():
            categories = self.repo.get_all_categories()
            category_id = categories[0][0]
            content_links = 'abc'
            response = self.repo.update_category(
                category_id,
                "name",
                "description",
                content_links)
        self.assertFalse(response)

        with self.app.app_context():
            categories = self.repo.get_all_categories()
            category_id = categories[0][0]
            content_links = [{"url": "https://www.eficode.com/cases/hansen", "type": "Case Study"}, {
                "url": "https://www.eficode.com/cases/basware", "type": "Case Study"}]
            response = self.repo.update_category(
                category_id,
                "name",
                "description",
                content_links)
        self.assertFalse(response)

    def test_delete_category_deletes_existing_category(self):
        with self.app.app_context():
            content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
            category_id = self.repo.create_category(
                "1",
                "name",
                "description",
                content_links)
            response1 = self.repo.delete_category(category_id)
            self.assertTrue(response1)
            response2 = self.repo.get_category(category_id)
            self.assertFalse(response2)

    def test_delete_category_with_invalid_arguments(self):
        with self.app.app_context():
            response = self.repo.delete_category('abc')
            self.assertFalse(response)

    def test_admin_exists_returns_true_when_admin_found(self):
        email = getenv('ADMIN_EMAIL_2')
        with self.app.app_context():
            response = self.repo._admin_exists(email)
        self.assertTrue(response)

    def test_admin_exists_returns_false_when_admin_not_found(self):
        email = "noemail@gmail.com"
        with self.app.app_context():
            response = self.repo._admin_exists(email)
        self.assertFalse(response)

    def test_add_admin_does_not_add_email_if_email_found_in_db(self):
        email = getenv('ADMIN_EMAIL_1')
        with self.app.app_context():
            response = self.repo.add_admin(email)
        self.assertIsNone(response)

    def test_get_categories_of_survey_returns_multiple_categories(self):
        with self.app.app_context():
            survey_id = 1
            response = self.repo.get_categories_of_survey(survey_id)

        self.assertGreater(len(response), 2)

    def test_get_categories_of_survey_returns_empty_list_if_survey_has_no_categories(self):
        with self.app.app_context():
            survey_id = 2
            response = self.repo.get_categories_of_survey(survey_id)
        self.assertEqual(len(response), 0)

    def test_sucessful_update_category_returns_category(self):
        with self.app.app_context():
            content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
            category_id = self.repo.create_category(
                "1",
                "name",
                "description",
                content_links)
            updated_category = self.repo.update_category(
                category_id,
                content_links,
                "A more descriptive name",
                "An actual description")
        self.assertTrue(updated_category != None)
        self.assertEquals(updated_category, category_id)

    def test_create_category_result(self):
        with self.app.app_context():
            category_id = self.repo.create_category(
                1, "cat", "cat is for category", [])
            text = "Category result text"
            cutoff_from_maxpts = 1.0
            category_result_id = self.repo.create_category_result(
                category_id,
                text,
                cutoff_from_maxpts)
            related_category_results = self.repo.get_category_results_from_category_id(category_id)[
                0]
            print(related_category_results, " - ", related_category_results[0])
            self.assertEquals(related_category_results[0], category_result_id)
            self.assertEquals(
                related_category_results[1], "Category result text")
            self.assertEquals(related_category_results[2], 1.0)

    def test_category_can_contain_multiple_category_results(self):
        with self.app.app_context():
            category_id = self.repo.create_category(
                1, "cat", "cat is for category", [])
            text = "Category result text 1"
            cutoff_from_maxpts = 1.0
            self.repo.create_category_result(
                category_id,
                text,
                cutoff_from_maxpts
            )

            text = "Category result text 2"
            cutoff_from_maxpts = 0.7
            self.repo.create_category_result(
                category_id,
                text,
                cutoff_from_maxpts
            )

            related_category_results = self.repo.get_category_results_from_category_id(
                category_id)
            self.assertTrue(len(related_category_results) == 2)

    def test_category_result_is_not_created_if_cutoff_exists(self):
        with self.app.app_context():
            category_id = self.repo.create_category(
                1, "cat", "cat is for category", [])
            text = "Category result text 1"
            cutoff_from_maxpts = 1.0
            self.repo.create_category_result(
                category_id,
                text,
                cutoff_from_maxpts
            )

            text = "Category result text 2"
            duplicate_cutoff = 1.0
            result = self.repo.create_category_result(
                category_id,
                text,
                duplicate_cutoff
            )
            self.assertIsNone(result)

    def test_create_a_survey_result_with_unique_cutoff_value(self):
        with self.app.app_context():
            result_id = self.repo.create_survey_result(
                8, "You seem to be an African elephant", 1.0)
        self.assertTrue(result_id)

    def test_survey_result_needs_to_have_unique_cutoff_value(self):
        with self.app.app_context():
            result_id = self.repo.create_survey_result(
                8, "You look like an Indian elephant", 1.0)
        self.assertFalse(result_id)

    def test_get_survey_results_returns_correct_amount_of_results(self):
        with self.app.app_context():
            self.repo.create_survey_result(
                8, "You look like an Indian elephant", 0.5)
            results = self.repo.get_survey_results(8)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[1][1], "You seem to be an African elephant")
        self.assertEqual(results[0][1], "You look like an Indian elephant")

    def test_delete_survey_result_deletes_survey_result(self):
        with self.app.app_context():
            self.repo.create_survey_result(
                8, "You look like an Indian elephant", 0.5)
            results = self.repo.get_survey_results(8)
            self.assertEqual(len(results), 2)

            response = self.repo.delete_survey_result(results[0][0])
            self.assertTrue(response)
            results = self.repo.get_survey_results(8)
            self.assertEqual(len(results), 1)

    def test_update_survey_results_updates_results_correctly(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey("Goodness", "How good are you",
                                                "Are you good? Or perhaps just decent?")
            original_results = [["Bad", 0.3], ["Good", 0.6], ["Great", 1.0]]
            new_results = [["Decent", 0.4], ["Great", 0.7], ["Fantastic", 1.0]]
            result_ids = []
            for result in original_results:
                result_ids.append(self.repo.create_survey_result(
                    survey_id, result[0], result[1]))
            or2 = []
            nr2 = []
            for i in range(3):
                or2.append(
                    (result_ids[i], original_results[i][0], original_results[i][1]))
                nr2.append(
                    (result_ids[i], new_results[i][0], new_results[i][1]))
            self.repo.update_survey_results(or2, nr2, survey_id)
            results = self.repo.get_survey_results(survey_id)
            self.assertEqual(results, nr2)

    def test_delete_category_result_deletes_category_result(self):
        with self.app.app_context():
            category_id = self.repo.create_category(
                1, "cat", "cat is for category", [])
            text = "Category result deletion test"
            cutoff_from_maxpts = 1.0
            category_result_id = self.repo.create_category_result(
                category_id,
                text,
                cutoff_from_maxpts)

            response = self.repo.get_category_results_from_category_result_id(
                category_result_id)
            self.assertEqual(len(response), 1)

            response = self.repo.delete_category_result(category_result_id)
            self.assertTrue(response)

            response = self.repo.get_category_results_from_category_result_id(
                category_result_id)
            self.assertIsNone(response)

            response = self.repo.delete_category_result('xxx')
            self.assertFalse(response)

    def test_update_category_result(self):
        with self.app.app_context():
            category_id = self.repo.create_category(
                1, "category containing category results", "resulting in successful testing", [])
            original_results = [["Bad", 0.3], ["Good", 0.6], ["Great", 1.0]]
            new_results = [["Decent", 0.4], ["Great", 0.7], ["Fantastic", 1.0]]
            result_ids = []
            for result in original_results:
                result_ids.append(self.repo.create_category_result(
                    category_id, result[0], result[1]))
            or2 = []
            nr2 = []
            for i in range(3):
                or2.append(
                    (result_ids[i], original_results[i][0], original_results[i][1]))
                nr2.append(
                    (result_ids[i], new_results[i][0], new_results[i][1]))
            self.repo.update_category_results(or2, nr2, 1)
            results = self.repo.get_category_results_from_category_id(
                category_id)
            self.assertEqual(results, nr2)

    def test_category_is_removed_from_question_with_correct_input(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "cat weight removal test",
                "test removal",
                "test removal"
            )
            category_weights = '[{"category": "Koira", "multiplier": 5.0}, {"category": "Cat", "multiplier": -5.0}]'
            question_id = self.repo.create_question(
                "test for category weight removal",
                survey_id,
                category_weights
            )
            new_weights = '[{"category": "Koira", "multiplier": 5.0}]'
            result = self.repo.remove_category_from_question(
                question_id,
                new_weights
            )
            self.assertEqual(
                result,
                [{"category": "Koira", "multiplier": 5.0}]
            )

    def test_removing_category_from_question_returns_none_with_invalid_input(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "cat weight removal test",
                "test removal",
                "test removal"
            )
            category_weights = '[{"category": "Koira", "multiplier": 5.0}, {"category": "Cat", "multiplier": -5.0}]'
            question_id = self.repo.create_question(
                "test for category weight removal",
                survey_id,
                category_weights
            )
            new_weights = [{"category": "Koira", "multiplier": 2}]
            result = self.repo.remove_category_from_question(
                question_id,
                new_weights
            )
            self.assertIsNone(result)

    def test_all_category_results_are_deleted_with_found_id(self):
        with self.app.app_context():
            result = self.repo.delete_category_results_of_category(300)
            self.assertTrue(result)

    def test_update_category_in_questions(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey("Pets", "What is the best pet?",
                                                "Are you more of a cat or a dog person?")
            category_id = self.repo.create_category(survey_id, "Koira",
                                                    "You are a dog person", [])
            self.repo.create_category(survey_id, "Cat",
                                      "You are a cat person", [])
            category_weights = '[{"category": "Koira", "multiplier": 5.0}, {"category": "Cat", "multiplier": -5.0}]'
            question_id = self.repo.create_question("Do you like to train your pet?",
                                                    survey_id, category_weights)
            self.repo.update_category(
                category_id, [], "Dog", "You are a dog person")
            question = self.repo.get_question(question_id)
            assert question[3] == [{"category": "Dog", "multiplier": 5.0}, {
                "category": "Cat", "multiplier": -5.0}]
