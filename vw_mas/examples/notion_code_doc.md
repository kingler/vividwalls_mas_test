
## Add-Block
```js
import { Client } from "@notionhq/client"
import { config } from "dotenv"

config()

const pageId = process.env.NOTION_PAGE_ID
const apiKey = process.env.NOTION_API_KEY

const notion = new Client({ auth: apiKey })

/* 
---------------------------------------------------------------------------
*/

/**
 * Resources:
 * - Appending block children endpoint (notion.blocks.children.append(): https://developers.notion.com/reference/patch-block-children)
 * - Working with page content guide: https://developers.notion.com/docs/working-with-page-content
 */

async function main() {
  const blockId = pageId // Blocks can be appended to other blocks *or* pages. Therefore, a page ID can be used for the block_id parameter
  const newHeadingResponse = await notion.blocks.children.append({
    block_id: blockId,
    // Pass an array of blocks to append to the page: https://developers.notion.com/reference/block#block-type-objects
    children: [
      {
        heading_2: {
          rich_text: [
            {
              text: {
                content: "Types of kale", // This is the text that will be displayed in Notion
              },
            },
          ],
        },
      },
    ],
  })

  // Print the new block(s) response
  console.log(newHeadingResponse)
}

main()
```
## Adding Linked Blocks

```json
import { Client } from "@notionhq/client"
import { config } from "dotenv"

config()

const pageId = process.env.NOTION_PAGE_ID
const apiKey = process.env.NOTION_API_KEY

const notion = new Client({ auth: apiKey })

/* 
---------------------------------------------------------------------------
*/

/**
 * Resources:
 * - Appending block children endpoint (notion.blocks.children.append(): https://developers.notion.com/reference/patch-block-children)
 * - Rich text options: https://developers.notion.com/reference/rich-text
 * - Working with page content guide: https://developers.notion.com/docs/working-with-page-content
 */

async function main() {
  const blockId = pageId // Blocks can be appended to other blocks *or* pages. Therefore, a page ID can be used for the block_id parameter
  const linkedTextResponse = await notion.blocks.children.append({
    block_id: blockId,
    // Pass an array of blocks to append to the page: https://developers.notion.com/reference/block#block-type-objects
    children: [
      {
        heading_3: {
          rich_text: [
            {
              text: {
                content: "Tuscan  kale", // This is the text that will be displayed in Notion
              },
            },
          ],
        },
      },
      {
        paragraph: {
          rich_text: [
            {
              text: {
                content:
                  "Tuscan  kale is a variety of kale with a long tradition in Italian cuisine, especially that of Tuscany. It is also known as Tuscan kale, Italian kale, dinosaur kale, kale, flat back kale, palm tree kale, or black Tuscan palm.",
                link: {
                  // Include a url to make the paragraph a link in Notion
                  url: "https://en.wikipedia.org/wiki/Kale",
                },
              },
            },
          ],
        },
      },
    ],
  })

  // Print the new block(s) response
  console.log(linkedTextResponse)
}

main()

```

## Create Notion Database

```json
import { Client } from "@notionhq/client"
import { config } from "dotenv"

config()

const pageId = process.env.NOTION_PAGE_ID
const apiKey = process.env.NOTION_API_KEY

const notion = new Client({ auth: apiKey })

/* 
---------------------------------------------------------------------------
*/

/**
 * Resources:
 * - Create a database endpoint (notion.databases.create(): https://developers.notion.com/reference/create-a-database)
 * - Working with databases guide: https://developers.notion.com/docs/working-with-databases
 */

async function main() {
  // Create a new database
  const newDatabase = await notion.databases.create({
    parent: {
      type: "page_id",
      page_id: pageId,
    },
    title: [
      {
        type: "text",
        text: {
          content: "New database name",
        },
      },
    ],
    properties: {
      // These properties represent columns in the database (i.e. its schema)
      "Grocery item": {
        type: "title",
        title: {},
      },
      Price: {
        type: "number",
        number: {
          format: "dollar",
        },
      },
      "Last ordered": {
        type: "date",
        date: {},
      },
    },
  })

  // Print the new database response
  console.log(newDatabase)
}

main()

```

## Add A Page to Database

```js
import { Client } from "@notionhq/client"
import { config } from "dotenv"
import { propertiesForNewPages } from "./sampleData.js"

config()

const pageId = process.env.NOTION_PAGE_ID
const apiKey = process.env.NOTION_API_KEY

const notion = new Client({ auth: apiKey })

/* 
---------------------------------------------------------------------------
*/

/**
 * Resources:
 * - Create a database endpoint (notion.databases.create(): https://developers.notion.com/reference/create-a-database)
 * - Create a page endpoint (notion.pages.create(): https://developers.notion.com/reference/post-page)
 * - Working with databases guide: https://developers.notion.com/docs/working-with-databases
 */

async function addNotionPageToDatabase(databaseId, pageProperties) {
  const newPage = await notion.pages.create({
    parent: {
      database_id: databaseId,
    },
    properties: pageProperties,
  })
  console.log(newPage)
}

async function main() {
  // Create a new database
  const newDatabase = await notion.databases.create({
    parent: {
      type: "page_id",
      page_id: pageId,
    },
    title: [
      {
        type: "text",
        text: {
          content: "Grocery list",
        },
      },
    ],
    properties: {
      // These properties represent columns in the database (i.e. its schema)
      "Grocery item": {
        type: "title",
        title: {},
      },
      Price: {
        type: "number",
        number: {
          format: "dollar",
        },
      },
      "Last ordered": {
        type: "date",
        date: {},
      },
    },
  })

  // Print the new database's URL. Visit the URL in your browser to see the pages that get created in the next step.
  console.log(newDatabase.url)

  const databaseId = newDatabase.id
  // If there is no ID (if there's an error), return.
  if (!databaseId) return

  console.log("Adding new pages...")
  for (let i = 0; i < propertiesForNewPages.length; i++) {
    // Add a few new pages to the database that was just created
    await addNotionPageToDatabase(databaseId, propertiesForNewPages[i])
  }
}

main()

```
## Query Database

```javascript

import { Client } from "@notionhq/client"
import { config } from "dotenv"
import { propertiesForNewPages } from "./sampleData.js"

config()

const pageId = process.env.NOTION_PAGE_ID
const apiKey = process.env.NOTION_API_KEY

const notion = new Client({ auth: apiKey })

/* 
---------------------------------------------------------------------------
*/

/**
 * Resources:
 * - Create a database endpoint (notion.databases.create(): https://developers.notion.com/reference/create-a-database)
 * - Create a page endpoint (notion.pages.create(): https://developers.notion.com/reference/post-page)
 * - Working with databases guide: https://developers.notion.com/docs/working-with-databases
 * Query a database: https://developers.notion.com/reference/post-database-query
 * Filter database entries: https://developers.notion.com/reference/post-database-query-filter
 */

async function addNotionPageToDatabase(databaseId, pageProperties) {
  await notion.pages.create({
    parent: {
      database_id: databaseId,
    },
    properties: pageProperties, // Note: Page properties must match the schema of the database
  })
}

async function queryDatabase(databaseId) {
  console.log("Querying database...")
  // This query will filter database entries and return pages that have a "Last ordered" property that is more recent than 2022-12-31. Use multiple filters with the AND/OR options: https://developers.notion.com/reference/post-database-query-filter.
  const lastOrderedIn2023 = await notion.databases.query({
    database_id: databaseId,
    filter: {
      property: "Last ordered",
      date: {
        after: "2022-12-31",
      },
    },
  })

  // Print filtered results
  console.log('Pages with the "Last ordered" date after 2022-12-31:')
  console.log(lastOrderedIn2023)
}

async function main() {
  // Create a new database
  const newDatabase = await notion.databases.create({
    parent: {
      type: "page_id",
      page_id: pageId,
    },
    title: [
      {
        type: "text",
        text: {
          content: "Grocery list",
        },
      },
    ],
    properties: {
      // These properties represent columns in the database (i.e. its schema)
      "Grocery item": {
        type: "title",
        title: {},
      },
      Price: {
        type: "number",
        number: {
          format: "dollar",
        },
      },
      "Last ordered": {
        type: "date",
        date: {},
      },
    },
  })
  // Print the new database's URL. Visit the URL in your browser to see the pages that get created in the next step.
  console.log(newDatabase.url)

  const databaseId = newDatabase.id
  // If there is no ID (if there's an error), return.
  if (!databaseId) return

  console.log("Adding new pages...")
  for (let i = 0; i < propertiesForNewPages.length; i++) {
    // Add a few new pages to the database that was just created
    await addNotionPageToDatabase(databaseId, propertiesForNewPages[i])
  }

  // After adding pages, query the database entries (pages)
  queryDatabase(databaseId)
}

main()

```

## Filter Sort Database

```javascript

import { Client } from "@notionhq/client"
import { config } from "dotenv"
import { propertiesForNewPages } from "./sampleData.js"

config()

const pageId = process.env.NOTION_PAGE_ID
const apiKey = process.env.NOTION_API_KEY

const notion = new Client({ auth: apiKey })

/* 
---------------------------------------------------------------------------
*/

/**
 * Resources:
 * - Create a database endpoint (notion.databases.create(): https://developers.notion.com/reference/create-a-database)
 * - Create a page endpoint (notion.pages.create(): https://developers.notion.com/reference/post-page)
 * - Working with databases guide: https://developers.notion.com/docs/working-with-databases
 * Query a database: https://developers.notion.com/reference/post-database-query
 * Filter database entries: https://developers.notion.com/reference/post-database-query-filter
 * Sort database entries: https://developers.notion.com/reference/post-database-query-sort
 */

async function addNotionPageToDatabase(databaseId, pageProperties) {
  await notion.pages.create({
    parent: {
      database_id: databaseId,
    },
    properties: pageProperties, // Note: Page properties must match the schema of the database
  })
}

async function queryAndSortDatabase(databaseId) {
  console.log("Querying database...")
  // This query will filter and sort database entries. The returned pages will have a "Last ordered" property that is more recent than 2022-12-31. Any database property can be filtered or sorted. Pass multiple sort objects to the "sorts" array to apply more than one sorting rule.
  const lastOrderedIn2023Alphabetical = await notion.databases.query({
    database_id: databaseId,
    filter: {
      property: "Last ordered",
      date: {
        after: "2022-12-31",
      },
    },
    sorts: [
      {
        property: "Grocery item",
        direction: "descending",
      },
    ],
  })

  // Print filtered/sorted results
  console.log(
    'Pages with the "Last ordered" date after 2022-12-31 in descending order:'
  )
  console.log(lastOrderedIn2023Alphabetical)
}

async function main() {
  // Create a new database
  const newDatabase = await notion.databases.create({
    parent: {
      type: "page_id",
      page_id: pageId,
    },
    title: [
      {
        type: "text",
        text: {
          content: "Grocery list",
        },
      },
    ],
    properties: {
      // These properties represent columns in the database (i.e. its schema)
      "Grocery item": {
        type: "title",
        title: {},
      },
      Price: {
        type: "number",
        number: {
          format: "dollar",
        },
      },
      "Last ordered": {
        type: "date",
        date: {},
      },
    },
  })
  // Print the new database's URL. Visit the URL in your browser to see the pages that get created in the next step.
  console.log(newDatabase.url)

  const databaseId = newDatabase.id
  if (!databaseId) return

  console.log("Adding new pages...")
  for (let i = 0; i < propertiesForNewPages.length; i++) {
    // Add a few new pages to the database that was just created
    await addNotionPageToDatabase(databaseId, propertiesForNewPages[i])
  }

  // After adding pages, query the database entries (pages) and sort the results
  queryAndSortDatabase(databaseId)
}

main()

```

