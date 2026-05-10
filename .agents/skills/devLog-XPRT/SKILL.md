```markdown
# devLog-XPRT Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches the core development patterns and conventions used in the `devLog-XPRT` TypeScript codebase. It covers file organization, import/export styles, commit message habits, and testing approaches, providing clear guidelines and examples to maintain consistency and quality across the project.

## Coding Conventions

### File Naming
- Use **camelCase** for all file names.
  - Example: `userProfile.ts`, `logEntryManager.ts`

### Import Style
- Use **relative imports** for referencing modules within the project.
  - Example:
    ```typescript
    import { getUserProfile } from './userProfile';
    ```

### Export Style
- Use **named exports** for all modules.
  - Example:
    ```typescript
    // userProfile.ts
    export function getUserProfile(id: string) { ... }
    ```

### Commit Messages
- Commit messages are **freeform** (no enforced prefix or structure).
- Average commit message length is around 21 characters.
  - Example: `fix log entry bug`

## Workflows

### Adding a New Module
**Trigger:** When you need to introduce a new feature or utility.
**Command:** `/add-module`

1. Create a new file using camelCase naming (e.g., `featureName.ts`).
2. Implement your logic using TypeScript.
3. Export your functions or constants using named exports.
   ```typescript
   export function newFeature() { ... }
   ```
4. Import your module in other files using relative imports.
   ```typescript
   import { newFeature } from './featureName';
   ```
5. Add corresponding tests in a `.test.ts` file.

### Writing and Running Tests
**Trigger:** When you add or update code and need to verify correctness.
**Command:** `/run-tests`

1. Create a test file with the same base name as the module, using `.test.ts` suffix.
   - Example: `userProfile.test.ts`
2. Write your tests (framework is currently unknown; follow existing patterns).
3. Run the test suite using the project's preferred test runner (check documentation or scripts).

### Making a Commit
**Trigger:** After completing a logical unit of work.
**Command:** `/commit`

1. Stage your changes.
2. Write a concise, freeform commit message (~21 characters recommended).
   - Example: `add user profile fetch`
3. Commit your changes.

## Testing Patterns

- Test files are named with the pattern `*.test.ts`.
- The testing framework is not specified; follow the structure of existing test files.
- Place tests alongside the modules they test or in a dedicated `tests` directory if present.

  Example:
  ```typescript
  // userProfile.test.ts
  import { getUserProfile } from './userProfile';

  test('returns correct user', () => {
    expect(getUserProfile('123')).toEqual({ id: '123', name: 'Alice' });
  });
  ```

## Commands
| Command      | Purpose                                      |
|--------------|----------------------------------------------|
| /add-module  | Scaffold and add a new module                |
| /run-tests   | Run the test suite for the codebase          |
| /commit      | Make a commit with a concise message         |
```
