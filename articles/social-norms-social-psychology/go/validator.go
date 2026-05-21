package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

var requiredColumns = []string{
	"participant", "session_id", "scenario_id", "site_id", "reference_group", "policy_domain",
	"condition", "trial", "descriptive_norm", "injunctive_norm", "empirical_expectation",
	"normative_expectation", "personal_attitude", "norm_salience", "sanction_salience",
	"sanction_severity", "reward_salience", "reference_group_identification",
	"institutional_legitimacy", "trust_in_institution", "pluralistic_ignorance",
	"dynamic_norm_trend", "message_type", "complied", "compliance_intention",
	"contribution_amount", "reported_violation", "response_time_ms", "norm_threshold",
	"tipping_exposure", "post_message_norm_perception",
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run go/validator.go data/social_norms_trials.csv")
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

		checkRange(row, index, "trial", 1, 1000000, line, &errors)
		checkRange(row, index, "complied", 0, 1, line, &errors)
		checkRange(row, index, "reported_violation", 0, 1, line, &errors)
		checkRange(row, index, "response_time_ms", 150, 10000000, line, &errors)
		checkRange(row, index, "dynamic_norm_trend", -100, 100, line, &errors)

		for _, col := range []string{
			"descriptive_norm", "injunctive_norm", "empirical_expectation",
			"normative_expectation", "personal_attitude", "pluralistic_ignorance",
			"compliance_intention", "contribution_amount", "norm_threshold",
			"tipping_exposure", "post_message_norm_perception",
		} {
			checkRange(row, index, col, 0, 100, line, &errors)
		}

		for _, col := range []string{
			"norm_salience", "sanction_salience", "sanction_severity", "reward_salience",
			"reference_group_identification", "institutional_legitimacy", "trust_in_institution",
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
