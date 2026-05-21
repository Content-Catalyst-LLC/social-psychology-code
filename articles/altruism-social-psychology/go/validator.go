package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

var requiredColumns = []string{
	"participant", "session_id", "recipient_id", "scenario_id", "site_id", "condition", "context_type", "trial",
	"empathy_score", "personal_distress", "helping_cost", "recipient_need", "recipient_closeness",
	"identity_overlap", "kinship_coefficient", "reciprocity_expectation", "reputation_visibility",
	"moral_identity", "social_norm_salience", "warm_glow_expectation", "perceived_efficacy",
	"intervention_risk", "altruistic_decision", "donation_amount", "time_volunteered_minutes",
	"altruistic_punishment", "punishment_cost", "public_goods_contribution", "response_time_ms",
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run go/validator.go data/altruism_trials.csv")
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
		checkRange(row, index, "kinship_coefficient", 0, 1, line, &errors)
		checkRange(row, index, "altruistic_decision", 0, 1, line, &errors)
		checkRange(row, index, "altruistic_punishment", 0, 1, line, &errors)
		checkRange(row, index, "donation_amount", 0, 100, line, &errors)
		checkRange(row, index, "punishment_cost", 0, 100, line, &errors)
		checkRange(row, index, "public_goods_contribution", 0, 100, line, &errors)
		checkRange(row, index, "time_volunteered_minutes", 0, 1000000, line, &errors)
		checkRange(row, index, "response_time_ms", 150, 10000000, line, &errors)

		for _, col := range []string{
			"empathy_score", "personal_distress", "helping_cost", "recipient_need",
			"recipient_closeness", "identity_overlap", "reciprocity_expectation",
			"reputation_visibility", "moral_identity", "social_norm_salience",
			"warm_glow_expectation", "perceived_efficacy", "intervention_risk",
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
