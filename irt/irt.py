"""
A simple, exploratory package for doing 1PL IRT. Note that all the functions
in this package are "negatives" of what you might expect because scipy only
has a minimize function, and not a maximize function.

@author Kevin Wilson - khwilson@gmail.com
@license Apache 2.0
"""
import numpy as np


def simulate(num_students, num_questions, num_responses_per_student):
    """
    Simulate a bunch of students responding sparsely to a bunch of questions,
    where student proficiencies and question difficulties are normally
    distributed about 0.0.

    :param int num_students: The number of students to simulate
    :param int num_questions: The number of questions to simulate
    :param int num_responses_per_student: The number of responses to simulate
            for each student (each question answered at most once).
    :return: The student proficiencies, the question difficulties, a
             num_students x num_responses array of which questions students
             answered, and a num_students x num_responses array of whether
             they got them correct.
    :rtype: np.ndarray[float], np.ndarray[float], np.ndarray[int], np.ndarray[bool]
    """
    thetas = np.random.randn(num_students)
    betas = np.random.randn(num_questions)
    answered = np.vstack([
        np.random.choice(num_questions, num_responses_per_student)
        for _ in xrange(num_students)])

    prob = 1.0 / (1.0 + np.exp(betas[answered] - thetas[:, np.newaxis]))
    correct = np.random.rand(*prob.shape) < prob

    return thetas, betas, answered, correct


def make_irt_neg_likelihood(answered, correct):
    """
    Return the negative of the likelihood function for 1PL IRT given the
    indices of questions answered and whether they were answered correctly.

    :param np.ndarray[int] answered: A num_students x num_responses array of the
            indices of questions that students answered
    :param np.ndarray[bool] correct: A num_students x num_responses array of
            whether the students answered those questions correctly.
    :return: The negative likelihood function
    :rtype: function
    """
    def likelihood(x):
        num_students, _ = answered.shape
        thetas = x[:num_students]
        betas = x[num_students:]

        logistic = 1.0 / (1.0 + np.exp(betas[answered] - thetas[:, np.newaxis]))
        return -(np.sum(logistic[correct]) + np.sum(1.0 - logistic[~correct]))

    return likelihood


def make_irt_neg_prior():
    """
    Return the negative of a normal prior on all of the student proficiencies
    and item difficulties.

    :return: The prior
    :rtype: function
    """
    def prior(x):
        return np.sum(np.square(x)) / 2.0

    return prior


def make_irt_neg_objective(answered, correct):
    """
    The objective is the sum of the posterior, i.e., the sum of the likelihood
    and the prior.

    :param np.ndarray[int] answered: A num_students x num_responses array of the
            indices of questions that students answered
    :param np.ndarray[bool] correct: A num_students x num_responses array of
            whether the students answered those questions correctly.
    :return: The negative of the posterior
    :rtype: function
    """
    likelihood = make_irt_neg_likelihood(answered, correct)
    prior = make_irt_neg_prior()
    return lambda x: likelihood(x) + prior(x)
