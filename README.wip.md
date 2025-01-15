# LinkML Antora generator

Generates an Antora module from a LinkML schema.

The generated module can then be made part of an Antora component version, playing its part in a larger piece of documentation.

NOTE: The generated AsciiDoc can also be used without Antora. See the section _If Antora is not desired_.

## Mapping

* LinkML schema -> Antora module
  * LinkML class -> Antora page (class template)
    * LinkML class attributes -> Antora page section
  * LinkML enumeration -> Antora page (enum template)
  * LinkML type -> Antora page (type template; _TODO_)
  * LinkML slots -> Antora page (_out of scope for now_)

## Limitations

* Non-attribute (top-level) slots are out of scope for now.

## If Antora is not desired

There's only two things that are Antora-specific:

* _File structure_. Files are structured as an Antora module, organizing all resources in so-called families.
* _Reference style_. Resources are referenced using Antora resource IDs.

### File structure

How the files are organized has no bearing on whether the files are used with Antora or not. If, however, you wish to restructure the files, all references need to be refactored of course.

### Reference style
Using the `--ref-style` parameter how the generator references resources can be configured:

* `antora`: Use Antora resource IDs for use with the Antora framework;
* `plain`: Use relative file paths for plain AsciiDoc style references.

## Benefits over alternatives

* Server-sided diagram rendering.
  * Avoids diagram code to match search queries and appear in search results.
  * Users never see diagram code when rendering has not finished yet.
  * No reliance on external services for availability of diagrams.
  * Avoids complicated architectures and keeps the website static and easy to work with.
* AsciiDoc partials generation for maximal reusability of documentation parts.

## Development

### Conventions

* I emphasize the use of hashable, immutable data types, and try to make everything deterministic using only data types that support ordering.
* If methods or functions start with a verb they have side effects (_pull_ or _push_). Otherwise, they are pure functions (_transformations_).
* Typenames are `UpperCamelCase` and try to encode a lot of context, whereas function names are `lower_snake_case` and are contextualized by their namespace.
** For example, the type `AntoraPage` is not abbreviated to just `Page` even though the namespace is `antora`.
