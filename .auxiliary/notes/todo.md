# Development TODOs

## Verification Tasks

- [ ] **Verify pickle/copy support**: Test and verify that all immutable types properly support Python's pickle protocol and copy module operations. Update documentation and requirements once verified.
  - Test pickling of Dictionary, ValidatorDictionary, Namespace
  - Test pickling of classes created with metaclasses
  - Test pickling of classes created with decorators
  - Test copy.copy() and copy.deepcopy() operations
  - Document any limitations or special considerations
