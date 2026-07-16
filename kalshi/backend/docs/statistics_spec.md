# this page marks the location for the General Statistics Rules of the project


## Core Principle

# in order to build more complex and robust models, these features must remain seperate:

- Player identity and statistics
- Event data
- Aggregate statistics
- Machine-Learning features

## Source of truth

Everything must be based on data. Without it everything is fictitious, raw and nominalized match events are at the core of the Source of Truth.

## Goal classifications

A single goal may belong to multiple classifications without counting as
more than one actual goal.

Example:

- total goals: +1
- direct free-kick goals: +1
- set-piece goals: +1
- long-range goals: +1
- weak-foot goals: +1

The underlying goal count remains one.

## Statistical layers

1. Raw provider data
2. Normalized match events
3. Match-level summaries
4. Season and career summaries
5. Machine-learning feature snapshots

## Metric categories

Metrics must be identified as:

- observed
- provider-calculated
- internally derived
- model-inferred

## Per-90 statistics

Per-90 statistics must be calculated from minutes played:

metric_per_90 = metric / minutes_played * 90

Totals, minutes and sample size must remain available alongside the
per-90 result.

## Time integrity

Every prediction feature must use an as-of timestamp.

A model must not receive information that became available after the
event it is predicting.

## Versioning

Derived and model-generated metrics should retain:

- source
- definition version
- calculation version
- calculated timestamp