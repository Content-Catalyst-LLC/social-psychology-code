package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

var requiredColumns = []string{
	"participant", "site_id", "condition", "trial", "target_group_relation",
	"ingroup_target", "group_identification", "identity_salience",
	"perceived_threat", "norm_strength", "status_asymmetry",
	"trust_rating", "fairness_rating", "competence_rating", "warmth_rating",
	"empathy_rating", "moral_blame", "moral_forgiveness",
	"punishment_severity", "reward_allocation", "resource_allocation",
	"cooperation_choice", "response_time_ms", "institutional_context",
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run go/validator.go data/ingroup_bias_trials.csv")
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
	relationCounts := map[string]int{}
	errors := 0

	for rowNum, row := range rows[1:] {
		line := rowNum + 2
		conditionCounts[row[index["condition"]]]++
		relationCounts[row[index["target_group_relation"]]]++

		checkRange(row, index, "trial", 1, 1000000, line, &errors)
		checkBinary(row, index, "ingroup_target", line, &errors)
		checkRange(row, index, "group_identification", 0, 10, line, &errors)
		checkRange(row, index, "identity_salience", 0, 10, line, &errors)
		checkRange(row, index, "perceived_threat", 0, 10, line, &errors)
		checkRange(row, index, "norm_strength", 0, 10, line, &errors)
		checkRange(row, index, "status_asymmetry", 0, 10, line, &errors)
		checkRange(row, index, "trust_rating", 0, 10, line, &errors)
		checkRange(row, index, "fairness_rating", 0, 10, line, &errors)
		checkRange(row, index, "competence_rating", 0, 10, line, &errors)
		checkRange(row, index, "warmth_rating", 0, 10, line, &errors)
		checkRange(row, index, "empathy_rating", 0, 10, line, &errors)
		checkRange(row, index, "moral_blame", 0, 10, line, &errors)
		checkRange(row, index, "moral_forgiveness", 0, 10, line, &errors)
		checkRange(row, index, "punishment_severity", 0, 10, line, &errors)
		checkRange(row, index, "reward_allocation", 0, 100, line, &errors)
		checkRange(row, index, "resource_allocation", 0, 100, line, &errors)
		checkBinary(row, index, "cooperation_choice", line, &errors)
		checkRange(row, index, "response_time_ms", 150, 1000000, line, &errors)
	}

	fmt.Printf("Validated file: %s\n", path)
	fmt.Printf("Rows checked: %d\n", len(rows)-1)
	fmt.Printf("Validation errors: %d\n", errors)
	fmt.Println("Condition counts:")
	for condition, count := range conditionCounts {
		fmt.Printf("  %s: %d\n", condition, count)
	}
	fmt.Println("Target relation counts:")
	for rel, count := range relationCounts {
		fmt.Printf("  %s: %d\n", rel, count)
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

func checkBinary(row []string, index map[string]int, col string, line int, errors *int) {
	value := row[index[col]]
	if value != "0" && value != "1" {
		fmt.Printf("Line %d: %s must be 0 or 1, got %s\n", line, col, value)
		*errors = *errors + 1
	}
}
