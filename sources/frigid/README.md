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

## Data Flow

### Initialization Flow

Immutable objects follow a consistent initialization pattern:

1. Object creation begins with `__new__`
2. During `__init__`, attributes/entries can be freely set
3. After `__init__` completes, protection activates via `__setattr__`/`__delattr__` overrides
4. Subsequent modification or deletion attempts raise immutability exceptions

For `ImmutableDictionary`, the `_behaviors_` set controls this: `'immutability'`
is absent during `__init__` (mutations allowed) and added after initialization.

### Dictionary Operation Flow

Set operations (union, intersection) maintain immutability guarantees:

1. User invokes operation: `dict1 | dict2`
2. Operation method computes new data (checks for key conflicts on union)
3. Method calls `with_data()` to create a new instance
4. New instance has the same type and validator (if applicable)
5. Returns a new immutable dictionary — originals are unchanged

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

## Sister Projects

- **[classcore](https://github.com/emcd/python-classcore)** — Foundational class factory and behavior system. Provides the metaclass machinery, attribute protection, and concealment that frigid delegates to.
- **[accretive](https://github.com/emcd/python-accretive)** — Grow-only data structures. Like frigid, but values can be added (never modified or removed) after creation. Useful for registries, plugin systems, and sticky-state configurations.
