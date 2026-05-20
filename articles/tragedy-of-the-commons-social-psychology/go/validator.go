package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

var requiredColumns = []string{
	"participant", "group_id", "site_id", "condition", "property_regime", "round",
	"resource_stock", "carrying_capacity", "regeneration_rate", "regeneration",
	"extraction", "sustainable_threshold", "trust_score", "legitimacy_score",
	"monitoring_credibility", "sanction_probability", "sanction_severity",
	"boundary_clarity", "rule_participation", "conflict_resolution_access",
	"local_ecological_knowledge", "perceived_fairness", "reciprocity_expectation",
	"stewardship_norm_salience", "asymmetry_index", "depletion_risk",
	"group_welfare", "individual_payoff", "response_time_ms",
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run go/validator.go data/tragedy_commons_trials.csv")
	}

	path := os.Args[1]
	file, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	reader.FieldsPerRecord = -1
	rows, err := reader.ReadAll()
	if err != nil {
		log.Fatal(err)
	}
	if len(rows) < 2 {
		log.Fatal("CSV must contain a header and at least one data row")
	}

	header := rows[0]
	index := map[string]int{}
	for i, col := range header {
		index[col] = i
	}

	missing := []string{}
	for _, col := range requiredColumns {
		if _, ok := index[col]; !ok {
			missing = append(missing, col)
		}
	}
	if len(missing) > 0 {
		log.Fatalf("Missing required columns: %v", missing)
	}

	errors := 0
	conditionCounts := map[string]int{}

	for rowNum, row := range rows[1:] {
		line := rowNum + 2
		conditionCounts[row[index["condition"]]]++

		checkRange(row, index, "round", 1, 1000000, line, &errors)
		checkRange(row, index, "resource_stock", 0, 1000000, line, &errors)
		checkRange(row, index, "carrying_capacity", 0, 1000000, line, &errors)
		checkRange(row, index, "regeneration_rate", 0, 100, line, &errors)
		checkRange(row, index, "regeneration", 0, 1000000, line, &errors)
		checkRange(row, index, "extraction", 0, 1000000, line, &errors)
		checkRange(row, index, "sustainable_threshold", 0, 1000000, line, &errors)
		checkRange(row, index, "sanction_probability", 0, 1, line, &errors)
		checkRange(row, index, "depletion_risk", 0, 1, line, &errors)
		checkRange(row, index, "response_time_ms", 150, 1000000, line, &errors)

		for _, col := range []string{
			"trust_score", "legitimacy_score", "monitoring_credibility",
			"sanction_severity", "boundary_clarity", "rule_participation",
			"conflict_resolution_access", "local_ecological_knowledge",
			"perceived_fairness", "reciprocity_expectation",
			"stewardship_norm_salience", "asymmetry_index",
		} {
			checkRange(row, index, col, 0, 10, line, &errors)
		}
	}

	fmt.Printf("Validated file: %s\n", path)
	fmt.Printf("Rows checked: %d\n", len(rows)-1)
	fmt.Printf("Validation errors: %d\n", errors)
	fmt.Println("Condition counts:")
	for condition, count := range conditionCounts {
		fmt.Printf("  %s: %d\n", condition, count)
	}

	if errors > 0 {
		os.Exit(2)
	}
}

func checkRange(row []string, index map[string]int, col string, min float64, max float64, line int, errors *int) {
	value, err := strconv.ParseFloat(row[index[col]], 64)
	if err != nil {
		fmt.Printf("Line %d: %s is not numeric: %s\n", line, col, row[index[col]])
		*errors = *errors + 1
		return
	}
	if value < min || value > max {
		fmt.Printf("Line %d: %s out of range [%.1f, %.1f]: %.3f\n", line, col, min, max, value)
		*errors = *errors + 1
	}
}
