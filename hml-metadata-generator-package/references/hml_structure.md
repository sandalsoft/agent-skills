# HML Metadata Structure Reference

This document provides detailed information about the structure and metadata fields for common Hasura DDN metadata objects found in .hml files.

## Common Metadata Object Kinds

### Model

Models represent collections of data objects (e.g., tables, views, queries).

**Key fields for description:**
- `definition.name` - The model name
- `definition.objectType` - The type of objects in this collection
- `definition.source` - Data source information (connector, collection)
- `definition.graphql` - GraphQL API configuration
- `definition.arguments` - Model arguments/parameters

**Description should include:**
- What the model represents
- The data source backing it
- Key operations supported (query, mutations)

**Example:**
```yaml
kind: Model
version: v1
definition:
  name: Users
  objectType: User
  description: "Model representing a collection of User objects backed by the 'users' table in the postgres connector. Supports operations to query multiple records and query by unique identifiers."
```

### ObjectType

Defines the structure of custom data types with fields.

**Key fields for description:**
- `definition.name` - The type name
- `definition.fields` - Array of field definitions
- `definition.dataConnectorTypeMapping` - Mapping to data connector types

**Field descriptions should include:**
- What the field represents
- Nullability status
- Whether it's an array
- Relationship to parent type

**Example:**
```yaml
kind: ObjectType
version: v1
definition:
  name: User
  description: "Type definition for User with 5 fields mapped to user."
  fields:
    - name: userId
      type: Int!
      description: "The user id for this User"
    - name: email
      type: String!
      description: "The email for this User"
    - name: createdAt
      type: Timestamp
      description: "The created at for this User (nullable)"
```

### Command

Commands represent operations or procedures (mutations, custom functions).

**Key fields for description:**
- `definition.name` - Command name
- `definition.outputType` - Return type
- `definition.arguments` - Input parameters
- `definition.source` - Data source information

**Description should include:**
- Purpose of the command
- Return type
- Key arguments
- Data connector

**Example:**
```yaml
kind: Command
version: v1
definition:
  name: CreateUser
  outputType: User
  description: "Command operation 'CreateUser' that returns User. Accepts 2 arguments: email, name via postgres connector."
```

### Relationship

Defines relationships between models.

**Key fields for description:**
- `definition.name` - Relationship name
- `definition.source` - Source model/type
- `definition.target` - Target model
- `definition.relationshipType` - Type (Object/Array)

**Example:**
```yaml
kind: Relationship
version: v1
definition:
  name: orders
  description: "Relationship 'orders' connecting User to Orders."
```

### BooleanExpressionType

Defines filtering expressions for queries.

**Key fields:**
- `definition.name` - Expression name
- `definition.operand` - Type being filtered
- `definition.logicalOperators` - AND, OR, NOT support
- `definition.comparableFields` - Filterable fields

**Example:**
```yaml
kind: BooleanExpressionType
version: v1
definition:
  name: User_bool_exp
  description: "Boolean expression type for filtering User objects."
```

### OrderByExpression

Defines sorting expressions.

**Example:**
```yaml
kind: OrderByExpression
version: v1
definition:
  name: User_order_by
  description: "Order by expression for sorting User objects."
```

### AggregateExpression

Defines aggregate operations (sum, avg, count, etc.).

**Example:**
```yaml
kind: AggregateExpression
version: v1
definition:
  name: User_aggregate_exp
  description: "Aggregate expression for computing aggregates on User."
```

## Best Practices for Descriptions

### Be Specific
- Include actual names from the metadata (model names, field names, types)
- Reference the data source when relevant
- Mention key operations or capabilities

### Be Concise
- One to two sentences for most descriptions
- Focus on what, not how
- Avoid redundant information

### Use Consistent Format
- Start with "Model representing..." for Models
- Start with "Type definition for..." for ObjectTypes
- Start with "Command operation..." for Commands
- Start with "The [field_name]..." for fields

### Include Context
- For fields: relationship to parent type
- For models: backing data source
- For commands: return type and key arguments
- For relationships: source and target

## Field Name Conventions

Convert technical names to readable descriptions:
- `userId` → "user id"
- `createdAt` → "created at"
- `orderTotal` → "order total"
- Handle underscores: `user_id` → "user id"

## Type Information

Include type information in field descriptions:
- Non-nullable: `Int!` → "The user id (integer)" or just omit nullability mention
- Nullable: `String` → "The email (nullable)"
- Arrays: `[String!]!` → "Array of strings representing the tags"

## Common Patterns

### Collection Models
"Model representing a collection of {Type} objects backed by the '{table}' collection in the {connector} connector."

### Lookup Models  
"Model representing a single {Type} object with lookup by unique identifier."

### Type Fields
"The {readable_name} for this {ParentType}{nullability_note}"

### Relationship Fields
"Relationship to {TargetModel} via {relationship_name}"

### Aggregate Fields
"Aggregated {field_name} computed across related {Type} objects"
