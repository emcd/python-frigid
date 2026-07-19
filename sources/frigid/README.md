# frigid

Immutable data structures for Python. Provides collections and class behaviors
that cannot be modified after creation.

## Architecture

Layered architecture with three tiers:

```
┌─────────────────────────────────────────────────┐
│  Public API                                      │
│  (Dictionary, Namespace, Object, decorators)     │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  Core Implementation (*/)                        │
│  (ImmutableDictionary, type aliases, doc frags)  │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  Foundation Libraries                            │
│  (classcore, dynadoc, absence)                   │
└─────────────────────────────────────────────────┘
```

All modules follow the `__` import pattern: public modules import from
`. import __`, which provides centralized access to external dependencies.

## Modules

### Public API (`sources/frigid/`)

| Module | Purpose |
|---|---|
| `__init__.py` | Package entry point; re-exports public API |
| `classes.py` | Metaclasses (`Class`, `Dataclass`, `AbstractBaseClass`, `Protocol*`) and decorators (`with_standard_behaviors`, `dataclass_with_standard_behaviors`) |
| `dictionaries.py` | `Dictionary`, `ValidatorDictionary` with set operations (`\|`, `&`) |
| `namespaces.py` | `Namespace` — like `SimpleNamespace`, but immutable |
| `modules.py` | `Module` type and `finalize_module()` utility |
| `sequences.py` | `one()` — single-item tuple factory |
| `exceptions.py` | `Omniexception` → `Omnierror` → `AttributeImmutability`, `EntryImmutability`, `EntryInvalidity` |
| `installers.py` | Utilities for installing into builtins |

### Internal (`sources/frigid/__/`)

| Module | Purpose |
|---|---|
| `imports.py` | Centralized external library imports |
| `nomina.py` | Type aliases, type variables, `calculate_attrname()` |
| `dictionaries.py` | `ImmutableDictionary` — core dict subclass with immutability enforcement |
| `doctab.py` | Documentation fragments table for dynadoc |
| `exceptions.py` | Internal exception classes |

## Key Patterns

**Wrapper Pattern**: `Dictionary` wraps `ImmutableDictionary` in `_data_`.
`Namespace` uses `ImmutableDictionary` for `__dict__`.

**Delegation Pattern**: Core immutability enforcement delegated to
`classcore.standard.class_factory`. Frigid provides configuration (attribute
naming, dynadoc, error classes) via `functools.partial`.

**Behavioral Flags**: `ImmutableDictionary` uses `_behaviors_` set to track
state. During `__init__`, immutability is not active. After `__init__`,
`'immutability'` is added to the set and all mutations are blocked.

**Template Method**: `Dictionary.with_data()` creates new instances with
same type and validator but different data. Subclasses override to maintain
behavior.

## Initialization Flow

1. Object creation begins with `__new__`
2. During `__init__`, attributes/entries can be freely set
3. After `__init__` completes, protection activates
4. Subsequent modification attempts raise immutability exceptions

## Dependencies

- **classcore** `~=1.10`: Class factory mechanism and attribute protection
- **dynadoc** `~=1.4`: Dynamic documentation generation with reusable fragments
- **absence** `~=1.1`: Sentinel for absent values (distinguishes missing from `None`)
- **typing-extensions**: Backported typing features

## Exception Hierarchy

```
Omniexception (BaseException)
└── Omnierror (Exception)
    ├── AttributeImmutability (+ AttributeError)
    ├── EntryImmutability (+ TypeError)
    ├── EntryInvalidity (+ ValueError)
    └── ErrorProvideFailure (+ RuntimeError)
```

Dual inheritance allows catching via frigid's hierarchy or Python built-ins.
