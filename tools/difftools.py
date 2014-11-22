"""
Some tools to aid in finite-difference testing of derivatives.

@author Kevin Wilson - khwilson@gmail.com
@license Apache 2.0
"""
def finite_difference_test(f, grad, num_args,
                           left_bound=-1.0, right_bound=1.0,
                           num_tests=20, eps=1e-6, decimal=6):
    """
    Given a function from an np.nadarry of length num_args to a scalar and
    a function that represents its gradient, assert whether it passes a
    finite difference test.

    :param function f: The function whose derivative you'd like to check. Should
            take an np.ndarray of size num_args and return a scalar
    :param function grad: The purported derivative of f. Should take an
            np.ndarray of size num_args and return an np.ndarray of size num_args.
    :param int num_args: The number of arguments f takes
    :param float left_bound: The left side of the interval on which we will
            do the finite-difference test
    :param float right_bound: The right side of the interval on which we will
            do the finite-differnce test
    :param int num_tests: The number of random tests to run
    :param float eps: The finite difference
    :param int decimal: The number of decimal places to which the finite-difference
            gradient and grad must agree
    """
    for num_test in xrange(num_tests):
        args = (right_bound - left_bound) * np.random.random(num_args) + left_bound
        actual_grad = grad(args)
        expected_grad = np.empty_like(args)
        for i in xrange(expected_grad.size):
            args[i] += eps
            upper = f(args)
            args[i] -= 2 * eps
            lower = f(args)
            args[i] += eps
            expected_grad[i] = (upper - lower) / 2.0 / eps

        assert np.testing.assert_array_almost_equal(expected_grad,
                                                    actual_grad,
                                                    decimal=decimal)


def finite_difference_vec_test(f, grad, num_args,
                               left_bound=-1.0, right_bound=1.0,
                               num_tests=20, eps=1e-6, decimal=6):
    """
    Given a function from an np.nadarry of length num_args to an np.ndarray
    (of size say num_target) an a function that represents its gradient (of size
    num_target x num_args), assert whether it passes a finite difference test.

    :param function f: The function whose derivative you'd like to check. Should
            take an np.ndarray of size num_args and return an np.ndarray
    :param function grad: The purported derivative of f. Should take an
            np.ndarray of size num_args and return an np.ndarray of size
            num_target x num_args.
    :param int num_args: The number of arguments f takes
    :param float left_bound: The left side of the interval on which we will
            do the finite-difference test
    :param float right_bound: The right side of the interval on which we will
            do the finite-differnce test
    :param int num_tests: The number of random tests to run
    :param float eps: The finite difference
    :param int decimal: The number of decimal places to which the
            finite-difference gradient and grad must agree
    """
    args = (right_bound - left_bound) * np.random.random(num_args) + left_bound
    output = f(args)
    num_target = output.size

    for num_test in xrange(num_tests):
        args = (right_bound - left_bound) * np.random.random(num_args) + left_bound
        actual_grad = grad(args)
        expected_grad = np.empty_like(args)
        for i in xrange(args.size):
            args[i] += eps
            upper = f(args)
            args[i] -= 2 * eps
            lower= f(args)
            args[i] += eps
            expected_grad[:, i] = (upper - lower) / 2.0 / eps

    np.testing.assert_array_almost_equal(expected_grad,
                                         actual_grad,
                                         decimal=decimal)
