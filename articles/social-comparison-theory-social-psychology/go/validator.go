package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

var requiredColumns = []string{
	"participant", "site_id", "condition", "trial", "comparison_type",
	"comparison_domain", "reference_group", "self_standing", "reference_standing",
	"comparison_gap", "attainability", "similarity", "identity_relevance",
	"social_comparison_orientation", "self_eval_pre", "self_eval_post",
	"motivation_score", "envy", "inspiration", "discouragement", "reassurance",
	"self_esteem", "perceived_fairness", "relative_deprivation",
	"norm_perception", "digital_exposure", "response_time_ms",
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run go/validator.go data/social_comparison_trials.csv")
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

	conditionCounts := map[string]int{}
	typeCounts := map[string]int{}
	errors := 0

	for rowNum, row := range rows[1:] {
		line := rowNum + 2
		conditionCounts[row[index["condition"]]]++
		typeCounts[row[index["comparison_type"]]]++

		checkRange(row, index, "trial", 1, 1000000, line, &errors)
		checkRange(row, index, "self_standing", 0, 10, line, &errors)
		checkRange(row, index, "reference_standing", 0, 10, line, &errors)
		checkRange(row, index, "comparison_gap", -10, 10, line, &errors)
		checkRange(row, index, "attainability", 0, 10, line, &errors)
		checkRange(row, index, "similarity", 0, 10, line, &errors)
		checkRange(row, index, "identity_relevance", 0, 10, line, &errors)
		checkRange(row, index, "social_comparison_orientation", 0, 10, line, &errors)
		checkRange(row, index, "self_eval_pre", 0, 10, line, &errors)
		checkRange(row, index, "self_eval_post", 0, 10, line, &errors)
		checkRange(row, index, "motivation_score", 0, 10, line, &errors)
		checkRange(row, index, "envy", 0, 10, line, &errors)
		checkRange(row, index, "inspiration", 0, 10, line, &errors)
		checkRange(row, index, "discouragement", 0, 10, line, &errors)
		checkRange(row, index, "reassurance", 0, 10, line, &errors)
		checkRange(row, index, "self_esteem", 0, 10, line, &errors)
		checkRange(row, index, "perceived_fairness", 0, 10, line, &errors)
		checkRange(row, index, "relative_deprivation", 0, 10, line, &errors)
		checkRange(row, index, "norm_perception", 0, 10, line, &errors)
		checkRange(row, index, "digital_exposure", 0, 10, line, &errors)
		checkRange(row, index, "response_time_ms", 150, 1000000, line, &errors)
	}

	fmt.Printf("Validated file: %s\n", path)
	fmt.Printf("Rows checked: %d\n", len(rows)-1)
	fmt.Printf("Validation errors: %d\n", errors)
	fmt.Println("Condition counts:")
	for condition, count := range conditionCounts {
		fmt.Printf("  %s: %d\n", condition, count)
	}
	fmt.Println("Comparison type counts:")
	for typ, count := range typeCounts {
		fmt.Printf("  %s: %d\n", typ, count)
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
