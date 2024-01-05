# SimpleEventClustering

## Overview

This project aims to cluster events based on their similarity using a cosine similarity metric. The events are generated randomly, stored in a MongoDB database, and then clustered using a similarity threshold.

## Requirements

- Python 3.x
- MongoDB
- Required Python libraries (install via `pip install -r requirements.txt`):
  - scikit-learn
  - numpy
  - pymongo

## Project Structure

- `generate_random_event()`: Generates random events, stores them in both a JSON file (`events.json`) and a MongoDB collection (`events`).

- `filter_events(events)`: Filters unnecessary keys from the events based on a predefined set of required keys.

- `filter_stored_events()`: Reads events from `events.json`, filters them using `filter_events()`, and stores the filtered events in a new JSON file (`filtered_events.json`).

- `similarity_score(event1, event2)`: Calculates the cosine similarity score between two events based on their text representations.

- `createCollection(name)`: Creates a MongoDB collection with the given name.

- `event_compare(event_new, event_cluster)`: Compares a new event with an existing cluster based on the similarity score.

- `clear_database()`: Drops the entire `clusterdb` MongoDB database.

- `average_event(collection_name)`: Computes the average event for a given cluster.

- `clustering(event)`: Performs event clustering by comparing the new event with existing clusters and creating a new cluster if necessary.

## Usage

1. Install the required dependencies mentioned in the `requirements.txt` file.
2. Ensure that MongoDB is installed and running on your local machine.
3. Run the script using `python your_script_name.py` to generate random events, filter them, and perform event clustering.

## Example

```python
# Import the necessary functions
from your_script_name import generate_random_event, filter_stored_events, clustering

# Generate random events and store them in MongoDB
events = generate_random_event()

# Filter stored events
filtered_events = filter_stored_events()

# Perform event clustering
for event in filtered_events:
    clustering(event)
