The mock services are 2 pieces of python code that produce and transfer news articles from one location to another.
Together, they are able to simulate many of the interaction happening in the real framework.

As an example, run_test.sh has a setup that runs 2 pipelines concurrently: 
- web collection -> sentiment; and 
- spanish web collection -> translation -> sentiment.

To run this test, simply call:
$ ./run_test.sh N
where N is one of the "scale" parameters for the tests. Other parameters (number of cores and running time) can be set up directly inside run_test.sh.
As a reference, N = 100 runs a small test with around 50 articles created and processed, while N = 10000 runs a larger test with about 4500 articles processed.    
Feel free to play around with the parameters in run_test.sh and check how it influences the tests.

Two other utilities are included:
$ ./check_status.sh
that counts the number of articles processed by task; and
$ ./reseet_env.sh
that deletes all processed articles and basically resets the environment, making it ready for a fresh re-run of run_test.sh.
(There's no need to reset the environment, but check_status.sh will now count results from both runs.

Other services (Search, Newsfeed, etc) will be added in the future.
