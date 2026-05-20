package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

var requiredColumns = []string{
	"participant", "dyad_id", "site_id", "condition", "round", "horizon_type",
	"own_choice", "partner_choice", "cooperate", "partner_cooperate",
	"own_payoff", "partner_payoff", "cumulative_payoff",
	"temptation_payoff", "reward_payoff", "punishment_payoff", "sucker_payoff",
	"trust_score", "fairness_score", "expected_partner_cooperation",
	"communication_access", "punishment_available", "reputation_visibility",
	"monitoring_strength", "institutional_enforcement", "social_identity_salience",
	"response_time_ms",
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: go run go/validator.go data/prisoners_dilemma_trials.csv")
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
	errors := 0

	for rowNum, row := range rows[1:] {
		line := rowNum + 2
		conditionCounts[row[index["condition"]]]++

		checkRange(row, index, "round", 1, 1000000, line, &errors)
		checkRange(row, index, "cooperate", 0, 1, line, &errors)
		checkRange(row, index, "partner_cooperate", 0, 1, line, &errors)
		checkRange(row, index, "communication_access", 0, 1, line, &errors)
		checkRange(row, index, "punishment_available", 0, 1, line, &errors)

		for _, col := range []string{
			"trust_score", "fairness_score", "expected_partner_cooperation",
			"reputation_visibility", "monitoring_strength", "institutional_enforcement",
			"social_identity_salience",
		} {
			checkRange(row, index, col, 0, 10, line, &errors)
		}
		checkRange(row, index, "response_time_ms", 150, 1000000, line, &errors)

		T := mustParse(row[index["temptation_payoff"]])
		R := mustParse(row[index["reward_payoff"]])
		P := mustParse(row[index["punishment_payoff"]])
		S := mustParse(row[index["sucker_payoff"]])

		if !(T > R && R > P && P > S) {
			fmt.Printf("Line %d: payoff ordering does not satisfy T > R > P > S\n", line)
			errors++
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

func mustParse(value string) float64 {
	v, err := strconv.ParseFloat(value, 64)
	if err != nil {
		return 0
	}
	return v
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
