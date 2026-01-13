// npm install @mendable/firecrawl-js
import Firecrawl from '@mendable/firecrawl-js';

const app = new Firecrawl({ apiKey: "fc-c4914b55239c41b294ec14c3934944e7"  });

// Perform a search:
app.scrape('firecrawl.dev')