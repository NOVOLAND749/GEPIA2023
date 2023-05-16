import GeneDetailType from "~/types/GeneDetailType";

const getStripPlotLink = (gene: GeneDetailType) => {
  return `/api/getStripPlot/${gene.gene_name}`;
};

export function getGenePlotLinks(gene: GeneDetailType) {
  return { StripPlot: getStripPlotLink(gene) };
}
