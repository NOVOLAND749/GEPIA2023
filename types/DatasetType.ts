export default interface DatasetType {
  id: number;
  db_name: string;
  tumor_sample_number: number;
  normal_sample_number: number;
  has_normal: boolean;
  description: string;
}
