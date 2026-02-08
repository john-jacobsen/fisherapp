test_that("load_knowledge_graph loads the bundled YAML", {
  graph <- load_knowledge_graph()
  expect_true(!is.null(graph$graph_metadata))
  expect_true(!is.null(graph$nodes))
  expect_true(length(graph$nodes) >= 8)
})

test_that("get_topic returns correct node", {
  topic <- get_topic("fraction_arithmetic")
  expect_equal(topic$id, "fraction_arithmetic")
  expect_equal(topic$status, "active")
})

test_that("get_topic errors on unknown topic", {
  expect_error(get_topic("nonexistent_topic"), "Topic not found")
})

test_that("get_prerequisites returns correct prereqs", {
  prereqs <- get_prerequisites("fraction_arithmetic")
  expect_equal(length(prereqs), 0)

  prereqs <- get_prerequisites("exponent_rules")
  expect_equal(prereqs, "fraction_arithmetic")

  prereqs <- get_prerequisites("order_of_operations")
  expect_true("fraction_arithmetic" %in% prereqs)
  expect_true("exponent_rules" %in% prereqs)
})

test_that("get_active_topics returns 8 active topics", {
  active <- get_active_topics()
  expect_equal(length(active), 8)
  expect_true("fraction_arithmetic" %in% active)
  expect_true("geometric_series" %in% active)
})

test_that("get_topic_order returns valid topological order", {
  order <- get_topic_order()
  expect_equal(length(order), 8)

  # fraction_arithmetic must come first (no prereqs)
  expect_equal(order[1], "fraction_arithmetic")

  # Each topic must appear after all its prereqs
  for (i in seq_along(order)) {
    prereqs <- get_prerequisites(order[i])
    for (p in prereqs) {
      p_idx <- which(order == p)
      expect_true(p_idx < i,
        info = paste(order[i], "should come after", p))
    }
  }
})
