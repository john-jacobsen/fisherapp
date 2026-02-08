# =============================================================================
# Knowledge Graph — Load and query algebra.yml
# =============================================================================

#' @importFrom yaml read_yaml

#' Load the algebra knowledge graph from YAML
#'
#' @param path Path to YAML file. If NULL, uses the bundled algebra.yml.
#' @return List with \code{graph_metadata} and \code{nodes}
#' @export
load_knowledge_graph <- function(path = NULL) {
  if (is.null(path)) {
    path <- system.file("knowledge_graph", "algebra.yml", package = "fisherapp")
    if (path == "") stop("Could not find bundled algebra.yml")
  }
  yaml::read_yaml(path)
}

#' Get a single topic node by ID
#'
#' @param topic_id Character topic ID
#' @param graph Optional pre-loaded knowledge graph (avoids re-reading YAML)
#' @return List representing the topic node
#' @export
get_topic <- function(topic_id, graph = NULL) {
  if (is.null(graph)) graph <- load_knowledge_graph()
  for (node in graph$nodes) {
    if (node$id == topic_id) return(node)
  }
  stop("Topic not found: ", topic_id)
}

#' Get prerequisite topic IDs for a topic
#'
#' @param topic_id Character topic ID
#' @param graph Optional pre-loaded knowledge graph
#' @return Character vector of prerequisite topic IDs
#' @export
get_prerequisites <- function(topic_id, graph = NULL) {
  node <- get_topic(topic_id, graph)
  prereqs <- node$prerequisites
  if (is.null(prereqs)) return(character(0))
  unlist(prereqs)
}

#' Get all active topic IDs
#'
#' @param graph Optional pre-loaded knowledge graph
#' @return Character vector of active topic IDs
#' @export
get_active_topics <- function(graph = NULL) {
  if (is.null(graph)) graph <- load_knowledge_graph()
  ids <- character()
  for (node in graph$nodes) {
    if (!is.null(node$status) && node$status == "active") {
      ids <- c(ids, node$id)
    }
  }
  ids
}

#' Get active topics in topological (dependency) order
#'
#' Uses Kahn's algorithm to produce a valid ordering where prerequisites
#' always appear before dependent topics.
#'
#' @param graph Optional pre-loaded knowledge graph
#' @return Character vector of topic IDs in dependency order
#' @export
get_topic_order <- function(graph = NULL) {
  if (is.null(graph)) graph <- load_knowledge_graph()

  active <- list()
  for (node in graph$nodes) {
    if (!is.null(node$status) && node$status == "active") {
      active[[node$id]] <- node
    }
  }

  active_ids <- names(active)

  # Build in-degree map (only count edges to other active nodes)
  in_degree <- setNames(rep(0L, length(active_ids)), active_ids)
  for (id in active_ids) {
    prereqs <- active[[id]]$prerequisites
    if (!is.null(prereqs)) {
      for (p in unlist(prereqs)) {
        if (p %in% active_ids) {
          in_degree[id] <- in_degree[id] + 1L
        }
      }
    }
  }

  # Kahn's algorithm
  queue <- names(in_degree[in_degree == 0L])
  result <- character()

  while (length(queue) > 0) {
    node_id <- queue[1]
    queue <- queue[-1]
    result <- c(result, node_id)

    # Find nodes that depend on this one
    for (id in active_ids) {
      prereqs <- unlist(active[[id]]$prerequisites)
      if (node_id %in% prereqs) {
        in_degree[id] <- in_degree[id] - 1L
        if (in_degree[id] == 0L) {
          queue <- c(queue, id)
        }
      }
    }
  }

  if (length(result) != length(active_ids)) {
    warning("Cycle detected in knowledge graph!")
  }

  result
}
