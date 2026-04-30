package main

import "fmt"

func identityWeightedValue(attributes []float64, weights []float64) float64 {
	total := 0.0
	for i := range attributes {
		total += attributes[i] * weights[i]
	}
	return total
}

func main() {
	attributes := []float64{0.8, 0.6, 0.4}
	weights := []float64{0.5, 0.3, 0.2}
	fmt.Printf("Identity-weighted value: %.3f\n", identityWeightedValue(attributes, weights))
}
