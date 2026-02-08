# =============================================================================
# Package load hook — Register all templates on package load
# =============================================================================

.onLoad <- function(libname, pkgname) {
  register_fraction_arithmetic_templates()
  register_exponent_rules_templates()
  register_order_of_operations_templates()
  register_summation_notation_templates()
  register_solving_equations_templates()
  register_logarithms_exponentials_templates()
  register_combinatorics_templates()
  register_geometric_series_templates()
}
