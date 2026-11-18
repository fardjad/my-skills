---
name: test-hygiene
description: >-
  Write, review, and prune automated tests that protect observable behavior
  without burdening reviewers. Use when adding features or tests, changing or
  deleting tests, fixing bugs, assessing coverage, choosing test levels or
  doubles, or dealing with slow, flaky, or bloated suites. Apply when a request
  only says to add tests or make sure something works.
---

# Test hygiene

Tests exist to give a human justified confidence that the right thing was built
and still works. Nothing else justifies a test. Coverage numbers, symmetry with
the code structure, and "more is safer" are not reasons.

## Why this matters with agents

When an agent writes the implementation, reviewing every line may not be
practical or the best use of a human's time. A focused test suite gives the
reviewer a way to answer two questions: *did we build the right thing?* and *can
we prove it works?* That only works if:

- **The suite is small enough to read.** Redundant tests make review harder
  and can hide the important ones.
- **Each test reads like a specification.** The name and body state a behavior,
  the edge case, and the expected result, without chasing helpers or fixtures.
- **The edge cases that matter are visibly present.** The reviewer should be
  able to spot a missing one without having to find it through noise.

Treat reviewer attention as the scarce resource. Every test you add spends it.
Every test you delete gives it back.

## Decide what to test

Use red/green/refactor. Before adding a test, identify the behavior or risk it
protects and the breakage that would make it fail. If an existing test at the
same or a lower level catches that breakage, do not add another. If the test
cannot add useful information, do not write it.

Confirm each new test fails against the broken behavior, then make it pass and
refactor. For a bug fix, write the test and see it fail before fixing the bug.

- Test observable behavior. A test should survive a refactor that preserves
  behavior and fail when that behavior breaks.
- Cover the happy path and plausible edge and error cases. Use a representative
  case per equivalence class rather than every input permutation.
- For a bug fix, test the invariant that should hold, not the incorrect
  behavior.
- Use concrete, independently derived expected values. Do not compute
  expectations with the same logic as the code under test.
- Do not test trivial getters, setters, passthroughs, declarations, or the
  language and framework themselves. Test library use when the integration is
  the risk.
- Do not test private methods directly or add test-only hooks to production
  code. If important logic is hard to reach, consider extracting a collaborator
  with a public interface.
- Use mocks to isolate slow, nondeterministic, or awkward dependencies. Do not
  assert on mock interactions; mocks are not the subject of the test.

## Choose the test level

Choose the cheapest level that can catch the risk. When choosing between levels,
state the tradeoff in speed, failure specificity, and predictive power. Use the
test pyramid as a guide, not a required shape.

- Use small, fast tests for logic, branches, calculations, and domain rules. A
  unit may include several collaborators; use real ones when practical.
- Use narrow integration tests wherever data is serialized or deserialized,
  including HTTP clients and handlers, databases, queues, and filesystems.
  Exercise one boundary at a time against the real dependency or a faithful
  stand-in. These tests catch errors such as wrong SQL or JSON shapes.
- Verify service fakes against the real service, or use provider-verified
  consumer contracts, so the fake cannot drift unnoticed.
- Keep end-to-end tests to a few core product journeys. Do not use them to
  repeat edge cases covered by smaller tests.

Do not try to cover combinations of logic through broad tests. Test the logic in
small tests and the boundaries in narrow integration or contract tests. Use
broad tests sparingly for confidence that essential journeys are wired together.

## Make tests readable

Name each test for its behavior and condition, such as
`rejects a refund larger than the original payment`. The list of names should
read like a specification. Keep the relevant inputs and concrete expected
values in the test. Hide irrelevant setup behind a well-named helper rather
than a fixture the reader has to decode. Some duplication is better than
obscuring the case.

Keep arrange, act, and assert in order. Focus each test on one condition and
make failures specific enough to identify the broken behavior. Apply the same
care to test code as production code.

## Prune as you work

When changing tests, inspect nearby tests and remove those that no longer earn
their place, including tests you did not write. Remove tests that:

- Duplicate the same failure coverage at the same or a lower level, or cover
  trivial code.
- Assert implementation details or mock interactions instead of behavior, or
  break on behavior-preserving refactors.
- Have never been seen to fail and have no identifiable failure they would
  catch.
- Are flaky when the cause cannot be fixed quickly, or are skipped, commented
  out, or expected to fail without a live reason.
- Assert removed behavior, or were edited to pass after a behavior change
  without checking the intended contract.

Update tests for intentional contract changes rather than blindly making them
pass. Remove a higher-level test when its assertions are fully covered lower
down. If lower-level coverage is missing, add it first. If a higher-level test
caught a bug that lower-level tests missed, add the lower-level test before
considering its removal.

Merge near-duplicates into one clear test or a small parameterized set when the
cases exercise the same behavior with different data. Do not keep a test just
because it was hard to write. Delete obsolete tests rather than leaving skips,
comments, or TODOs. If an old test's value is unclear, flag it instead of
deleting it.

Keep a feature's tests focused enough for a reviewer to read in one sitting. If
they grow beyond that, reconsider the test level and cut or consolidate. If you
are writing the tenth variation of the same check, stop. Use coverage reports
to find important gaps, not to hit a percentage.

Before finishing, check that new tests fail for the intended breakage and that
boundaries and fakes have appropriate integration or contract coverage. Keep any
end-to-end tests focused on core journeys. Tell the user what tests were added
and removed, and why.

## Sources

- Kent Beck, [Test Desiderata][beck].
- Ham Vocke, [The Practical Test Pyramid][vocke].
- J. B. Rainsberger, [Beware the Integrated Tests Scam][r].

[beck]: https://medium.com/@kentbeck_7670/test-desiderata-94150638a4b3
[vocke]: https://martinfowler.com/articles/practical-test-pyramid.html
[r]: https://blog.thecodewhisperer.com/permalink/integrated-tests-are-a-scam
