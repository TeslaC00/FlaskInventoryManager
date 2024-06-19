# API Documentation

## Supplier Model

**Description**: Represents a supplier in the system.

| Column     | Data Type | Allowed for Sorting | Allowed for Filtering | Allowed for Searching |
|------------|-----------|---------------------|-----------------------|-----------------------|
| id         | Integer   | No                  | No                    | No                    |
| name       | String    | Yes                 | Yes                   | Yes                   |
| GST_No     | String    | No                  | Yes                   | Yes                   |
| state_code | Integer   | Yes                 | Yes                   | No                    |
| state_name | String    | Yes                 | Yes                   | Yes                   |
| address    | Text      | No                  | No                    | Yes                   |

## ProductionLog Model

**Description**: Represents a log entry for production.

| Column            | Data Type | Allowed for Sorting | Allowed for Filtering | Allowed for Searching |
|-------------------|-----------|---------------------|-----------------------|-----------------------|
| id                | Integer   | No                  | No                    | No                    |
| production_date   | Date      | Yes                 | Yes                   | No                    |
| product_part_no   | Integer   | Yes                 | Yes                   | No                    |
| quantity_produced | Integer   | Yes                 | Yes                   | No                    |

## ProductScrap Model

**Description**: Represents a scrap record for a product.

| Column          | Data Type | Allowed for Sorting | Allowed for Filtering | Allowed for Searching |
|-----------------|-----------|---------------------|-----------------------|-----------------------|
| product_part_no | Integer   | No                  | Yes                   | Yes                   |
| quantity        | Integer   | Yes                 | Yes                   | No                    |
| date            | Date      | Yes                 | Yes                   | No                    |
| scrap_type      | Enum      | Yes                 | Yes                   | Yes                   |

## ProductMaterial Model

**Description**: Represents a relationship between a product and its materials.

| Column           | Data Type | Allowed for Sorting | Allowed for Filtering | Allowed for Searching |
|------------------|-----------|---------------------|-----------------------|-----------------------|
| product_part_no  | Integer   | No                  | Yes                   | No                    |
| material_part_no | Integer   | No                  | Yes                   | No                    |
| quantity         | Integer   | Yes                 | Yes                   | No                    |

## Product Model

**Description**: Represents a product in the inventory.

| Column   | Data Type | Allowed for Sorting | Allowed for Filtering | Allowed for Searching |
|----------|-----------|---------------------|-----------------------|-----------------------|
| part_no  | Integer   | No                  | No                    | No                    |
| name     | String    | Yes                 | Yes                   | Yes                   |
| unit     | Enum      | Yes                 | Yes                   | No                    |
| quantity | Integer   | Yes                 | Yes                   | No                    |
| price    | Float     | Yes                 | Yes                   | No                    |
| c_gst    | Float     | Yes                 | Yes                   | No                    |
| s_gst    | Float     | Yes                 | Yes                   | No                    |
| i_gst    | Float     | Yes                 | Yes                   | No                    |

## MaterialScrap Model

**Description**: Represents a scrap record for a material.

| Column           | Data Type | Allowed for Sorting | Allowed for Filtering | Allowed for Searching |
|------------------|-----------|---------------------|-----------------------|-----------------------|
| material_part_no | Integer   | No                  | Yes                   | No                    |
| quantity         | Integer   | Yes                 | Yes                   | No                    |
| scrap_type       | Enum      | Yes                 | Yes                   | No                    |
| date             | Date      | Yes                 | Yes                   | No                    |

## Material Model

**Description**: Represents a material in the inventory.

| Column   | Data Type | Allowed for Sorting | Allowed for Filtering | Allowed for Searching |
|----------|-----------|---------------------|-----------------------|-----------------------|
| part_no  | Integer   | No                  | No                    | No                    |
| name     | String    | Yes                 | Yes                   | Yes                   |
| unit     | Enum      | Yes                 | Yes                   | No                    |
| quantity | Integer   | Yes                 | Yes                   | No                    |

## ChallanItem Model

**Description**: Represents an item in a challan.

| Column           | Data Type | Allowed for Sorting | Allowed for Filtering | Allowed for Searching |
|------------------|-----------|---------------------|-----------------------|-----------------------|
| id               | Integer   | No                  | No                    | No                    |
| price            | Float     | Yes                 | Yes                   | Yes                   |
| quantity         | Integer   | Yes                 | Yes                   | Yes                   |
| challan_id       | Integer   | Yes                 | Yes                   | Yes                   |
| material_part_no | Integer   | Yes                 | Yes                   | Yes                   |

## Challan Model

**Description**: Represents a challan in the system.

| Column      | Data Type | Allowed for Sorting | Allowed for Filtering | Allowed for Searching |
|-------------|-----------|---------------------|-----------------------|-----------------------|
| id          | Integer   | No                  | No                    | No                    |
| challan_no  | Integer   | Yes                 | Yes                   | Yes                   |
| supplier_id | Integer   | Yes                 | Yes                   | Yes                   |
| total_price | Float     | Yes                 | Yes                   | Yes                   |
| date        | Date      | Yes                 | Yes                   | No                    |
| remarks     | Text      | No                  | No                    | Yes                   |

## Buyer Model

**Description**: Represents a buyer in the system.

| Column     | Data Type | Allowed for Sorting | Allowed for Filtering | Allowed for Searching |
|------------|-----------|---------------------|-----------------------|-----------------------|
| id         | Integer   | No                  | No                    | No                    |
| name       | String    | Yes                 | Yes                   | Yes                   |
| GST_No     | String    | No                  | Yes                   | Yes                   |
| state_code | Integer   | Yes                 | Yes                   | No                    |
| state_name | String    | Yes                 | Yes                   | Yes                   |
| address    | Text      | No                  | No                    | Yes                   |

## BillItem Model

**Description**: Represents an item in a bill.

| Column          | Data Type | Allowed for Sorting | Allowed for Filtering | Allowed for Searching |
|-----------------|-----------|---------------------|-----------------------|-----------------------|
| id              | Integer   | No                  | No                    | No                    |
| quantity        | Integer   | Yes                 | No                    | Yes                   |
| price           | Float     | Yes                 | No                    | Yes                   |
| c_gst           | Float     | Yes                 | No                    | No                    |
| s_gst           | Float     | Yes                 | No                    | No                    |
| i_gst           | Float     | Yes                 | No                    | No                    |
| bill_id         | Integer   | Yes                 | No                    | Yes                   |
| product_part_no | Integer   | Yes                 | Yes                   | Yes                   |

## Bill Model

**Description**: Represents a bill in the system.

| Column         | Data Type | Allowed for Sorting | Allowed for Filtering | Allowed for Searching |
|----------------|-----------|---------------------|-----------------------|-----------------------|
| id             | Integer   | No                  | No                    | No                    |
| buyer_id       | Integer   | Yes                 | Yes                   | No                    |
| total_price    | Float     | Yes                 | Yes                   | No                    |
| date           | Date      | Yes                 | Yes                   | No                    |
| purchase_order | String    | Yes                 | No                    | Yes                   |
| remarks        | Text      | No                  | No                    | Yes                   |

## AuditLog Model

**Description**: Represents an audit log entry. (ReadOnly for all users)

| Column            | Data Type | Allowed for Sorting | Allowed for Filtering | Allowed for Searching |
|-------------------|-----------|---------------------|-----------------------|-----------------------|
| id                | Integer   | No                  | No                    | No                    |
| table_name        | String    | Yes                 | Yes                   | Yes                   |
| table_primary_key | String    | Yes                 | Yes                   | No                    |
| column_name       | String    | Yes                 | Yes                   | No                    |
| old_value         | String    | Yes                 | Yes                   | No                    |
| new_value         | String    | Yes                 | Yes                   | No                    |
| username          | String    | Yes                 | Yes                   | Yes                   |
| change_timestamp  | DateTime  | Yes                 | Yes                   | No                    |
| action_type       | Enum      | Yes                 | No                    | No                    |
| remarks           | Text      | No                  | No                    | Yes                   |
