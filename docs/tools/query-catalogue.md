# Natural-Language Query Catalogue

Search across missions, resources, infrastructure and qualifications using ordinary words or a short question.

<div class="mcuk-tool" data-mcuk-tool="query-catalogue">
  <div class="mcuk-tool-controls">
    <label>
      Question or keywords
      <input data-role="query" type="search" placeholder="e.g. what needs a Railway Police Officer?">
    </label>
  </div>
  <div data-role="results" aria-live="polite"><p>Enter a question or keywords.</p></div>
</div>

## How it works

This is a deterministic evidence search, not a generative AI answer engine.

The browser:

1. extracts words and numbers from the query;
2. matches them against the generated search index;
3. ranks records by the number of matching terms;
4. returns only canonical repository entities.

It does not create facts, infer missing values or search the live game.

## Useful query patterns

```text
railway police officer
harbour bomb disposal
airfield mass casualty
recovery centre bus
coastguard mud training
mission 807
```

## Interpretation

A high score means more query terms matched the indexed record. It is not a confidence score and does not alter the evidence classification of the underlying record.
